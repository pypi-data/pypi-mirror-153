import requests
import datetime,threading
import pandas as pd
import numpy as np


supertrend_period = 10
supertrend_multiplier = 3

class utilities:

    def __init__(self):
        self.base_url = "https://api.greentecq.com/v2/paper/"
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain"}
        self.type = 2
        self.trading_day = None

    def get_expiry_kite(self):
        try:
            df_inst = pd.read_csv("https://api.kite.trade/instruments")
            df = df_inst[df_inst['segment'] == "NFO-OPT"]
            df = df[df['tradingsymbol'].str.startswith(
                "{}".format("BANKNIFTY"))]
            df['expiry'] = pd.to_datetime(df['expiry'])

            expirylist = list(set(df[['tradingsymbol', 'expiry']].sort_values(
                by=['expiry'])['expiry'].values))
            expirylist = np.array([np.datetime64(x, 'D') for x in expirylist])
            expirylist = np.sort(expirylist)
            today = np.datetime64('today', 'D') + np.timedelta64(0, 'D')
            expirylist = expirylist[expirylist >= today]
            expiry_index = 0
            next_expiry = expirylist[expiry_index]
            next_expiry = pd.to_datetime(str(next_expiry))

            return datetime.date(next_expiry.year, next_expiry.month, next_expiry.day)
        except Exception as e:
            print(e)
            return None

    def myround(self, x, base):
        return base * round(x/base)

    def roundtick(self, x):
        ticksize = 0.05
        return round(x/ticksize)*ticksize

    def get_url(self, url):
        response = requests.get(url)
        # print(response.text)
        content = response.content.decode("utf8")
        return content

    def send_telegram_message(self, token, receipt_id, message):
        try:
            URL = "https://api.telegram.org/bot{}/".format(token)
            url = URL + \
                "sendMessage?text={}&chat_id={}".format(message, receipt_id)
            # return self.get_url(url)
            processing_request = threading.Thread(target=self.get_url, args=(url,))
            processing_request.start()
            return True
        except:
            print("Error occured in sending telegram notification")

    def check_limit_long_count(self, orderBook, option_type=None):

        if option_type is not None:
            checkOrderBook = orderBook.loc[(orderBook['OT'] == option_type) & (orderBook['signal'] == "Long")
                                           & (orderBook['status'] == "open") & (orderBook['exit_time'].isnull())]
        else:
            checkOrderBook = orderBook.loc[(orderBook['signal'] == "Long") & (orderBook['exit_time'].isnull())
                                           & (orderBook['status'] == "open")]
        if len(checkOrderBook) > 0:
            return len(checkOrderBook)
        return 0

    def check_pending_long_count(self, orderBook, option_type=None):

        if option_type is not None:
            checkOrderBook = orderBook.loc[(orderBook['OT'] == option_type) & (orderBook['signal'] == "Long")
                                           & (orderBook['status'] == "pending") & (orderBook['exit_time'].isnull())]
        else:
            checkOrderBook = orderBook.loc[(orderBook['signal'] == "Long") & (orderBook['exit_time'].isnull())
                                           & (orderBook['status'] == "pending")]
        if len(checkOrderBook) > 0:
            return len(checkOrderBook)
        return 0

    def check_open_long_count(self, orderBook, option_type=None):

        # print(orderBook)
        if option_type is not None:
            checkOrderBook = orderBook.loc[(orderBook['OT'] == option_type) & (orderBook['signal'] == "Long")
                                           & (orderBook['status'] == "TRAD") & (orderBook['exit_time'].isnull())]
        else:
            checkOrderBook = orderBook.loc[(orderBook['signal'] == "Long") & (orderBook['exit_time'].isnull())
                                           & (orderBook['status'] == "TRAD")]
        # print(checkOrderBook)
        if len(checkOrderBook) > 0:
            return len(checkOrderBook)
        return 0

    def check_limit_short_count(self, orderBook, option_type=None):

        if option_type is not None:
            checkOrderBook = orderBook.loc[(orderBook['OT'] == option_type) & (orderBook['signal'] == "Short")
                                           & (orderBook['status'] == "open") & (orderBook['exit_time'].isnull())]
        else:
            checkOrderBook = orderBook.loc[(orderBook['signal'] == "Short") & (orderBook['exit_time'].isnull())
                                           & (orderBook['status'] == "open")]
        if len(checkOrderBook) > 0:
            return len(checkOrderBook)
        return 0

    def check_open_short_count(self, orderBook, option_type=None):
        if option_type is not None:
            checkOrderBook = orderBook.loc[(orderBook['OT'] == option_type) & (orderBook['signal'] == "Short")
                                           & (orderBook['status'] == "TRAD") & (orderBook['exit_time'].isnull())]
        else:
            checkOrderBook = orderBook.loc[(orderBook['signal'] == "Short") & (orderBook['exit_time'].isnull())
                                           & (orderBook['status'] == "TRAD")]

        if len(checkOrderBook) > 0:
            return len(checkOrderBook)
        return 0

    def print_live(self, text):
        print(text, end='\r', flush=True)

    def entry(self, args, instrument, entry_time, order_id, ltp, signal, status):
        try:
            if 'strategy_name' in args:
                if 'daily_execution_id' in args:
                    data = {
                        'strategy_name': args["strategy_name"],
                        'symbol': instrument.symbol,
                        'entry_date': entry_time,
                        'order_id': order_id,
                        'qty': args["quantity"] * 25,
                        'option_type': instrument.option_type,
                        'entry_price': ltp,
                        'signal': signal,
                        'status': status,
                        'daily_execution_id': args["daily_execution_id"],
                    }
                else:
                    data = {
                        'strategy_name': args["strategy_name"],
                        'symbol': instrument.symbol,
                        'entry_date': entry_time,
                        'order_id': order_id,
                        'qty': args["quantity"] * 25,
                        'option_type': instrument.option_type,
                        'entry_price': ltp,
                        'signal': signal,
                        'status': status,
                    }
                response = requests.post(
                    self.base_url+"entry", headers=self.headers, data=data)
                response_json = (response.json())
                return int(response_json['execution_id'])
        except Exception as e:
            print(e)

    def exit(self, args, execution_id, exit_time, order_id, ltp, remarks, profit, loss, mtm, mtm_high, mtm_low):
        try:
            data = {
                'execution_id':  execution_id,
                'exit_date': exit_time,
                'exit_order_id': order_id,
                'exit_qty': args["quantity"] * 25,
                'exit_price': ltp,
                'exit_status': 'complete',
                'remarks': remarks,
                'profit': profit,
                'loss': loss,
                'mtm': mtm,
                'mtm_high':  mtm_high,
                'mtm_low':  mtm_low,

            }
            response = requests.post(
                self.base_url+"exit", headers=self.headers, data=data)
            response_json = (response.json())

        except Exception as e:
            print(e)

    def execution(self, args):
        try:
            if self.type is None:
                execution_type = 2
            else:
                execution_type = self.type 

            if 'strategy_name' in args:
                if 'api_key' in args:
                    data = {
                        'strategy_name': args["strategy_name"],
                        'type': execution_type,
                        'trading_day' : self.trading_day,
                        'api_key': args["api_key"]
                    }
                else:
                    data = {
                        'strategy_name': args["strategy_name"],
                            'type': execution_type,
                            'trading_day' : self.trading_day,
                    }
                # print(data)
                response = requests.post(
                    self.base_url+"execution", headers=self.headers, data=data)
                response_json = (response.json())
                # print(response_json)
                return int(response_json['daily_execution_id'])
        except Exception as e:
            print(e)

    def log_update(self, args, mtm, high, low):
        try:
            if 'daily_execution_id' in args:
                data = {
                    'daily_execution_id': args["daily_execution_id"],
                    'mtm': mtm,
                    'high': high,
                    'low': low,
                    'date':  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                response = requests.post(
                    self.base_url+"update", headers=self.headers, data=data)
                response_json = (response.json())
        except Exception as e:
            print(e)

class Indicators:
    def __init__(self):
        self.base_url = "https://api.greentecq.com/v2/paper/"


    def EMA(self,df, base, target, period, alpha=False):
        """
        Function to compute Exponential Moving Average (EMA)
        Args :
            df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
            base : String indicating the column name from which the EMA needs to be computed from
            target : String indicates the column name to which the computed data needs to be stored
            period : Integer indicates the period of computation in terms of number of candles
            alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
        Returns :
            df : Pandas DataFrame with new column added with name 'target'
        """

        con = pd.concat([df[:period][base].rolling(
            window=period).mean(), df[period:][base]])

        if (alpha == True):
            # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
            df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
        else:
            # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
            df[target] = con.ewm(span=period, adjust=False).mean()

        df[target].fillna(0, inplace=True)
        return df

    def ATR(df, period, ohlc=['open', 'high', 'low', 'close']):
        """
        Function to compute Average True Range (ATR)
        Args :
            df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
            period : Integer indicates the period of computation in terms of number of candles
            ohlc: List defining OHLC Column names (default ['Open', 'High', 'low', 'Close'])
        Returns :
            df : Pandas DataFrame with new columns added for
                True Range (TR)
                ATR (ATR_$period)
        """
        atr = 'ATR_' + str(period)

        # Compute true range only if it is not computed and stored earlier in the df
        if not 'TR' in df.columns:
            df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
            df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
            df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

            df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

            df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

        # Compute EMA of true range using ATR formula after ignoring first row
        self.EMA(df, 'TR', atr, period, alpha=True)

        return df


    def adx(self,ohlc):

        n = 14  # book emphasises on 14 day ADX as higher as possible
        df2 = ohlc.copy()
        df2['H-L'] = abs(df2['high']-df2['low'])
        df2['H-PC'] = abs(df2['high']-df2['close'].shift(1))
        df2['L-PC'] = abs(df2['low']-df2['close'].shift(1))
        df2['TR'] = df2[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
        df2['DMplus'] = np.where((df2['high']-df2['high'].shift(1)) > (
            df2['low'].shift(1)-df2['low']), df2['high']-df2['high'].shift(1), 0)
        df2['DMplus'] = np.where(df2['DMplus'] < 0, 0, df2['DMplus'])
        df2['DMminus'] = np.where((df2['low'].shift(
            1)-df2['low']) > (df2['high']-df2['high'].shift(1)), df2['low'].shift(1)-df2['low'], 0)
        df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
        TRn = []
        DMplusN = []
        DMminusN = []
        TR = df2['TR'].tolist()
        DMplus = df2['DMplus'].tolist()
        DMminus = df2['DMminus'].tolist()
        for i in range(len(df2)):
            if i < n:
                TRn.append(np.NaN)
                DMplusN.append(np.NaN)
                DMminusN.append(np.NaN)
            elif i == n:
                TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
                DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
                DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
            elif i > n:
                TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
                DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
                DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
        df2['TRn'] = np.array(TRn)
        df2['DMplusN'] = np.array(DMplusN)
        df2['DMminusN'] = np.array(DMminusN)
        df2['DIplusN'] = 100*(df2['DMplusN']/df2['TRn'])
        df2['DIminusN'] = 100*(df2['DMminusN']/df2['TRn'])
        df2['DIdiff'] = abs(df2['DIplusN']-df2['DIminusN'])
        df2['DIsum'] = df2['DIplusN']+df2['DIminusN']
        df2['DX'] = 100*(df2['DIdiff']/df2['DIsum'])
        ADX = []
        DX = df2['DX'].tolist()
        for j in range(len(df2)):
            if j < 2*n-1:
                ADX.append(np.NaN)
            elif j == 2*n-1:
                ADX.append(df2['DX'][j-n+1:j+1].mean())
            elif j > 2*n-1:
                ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
        df2['ADX'] = np.array(ADX)
        # df3 = df2.loc[:,'DIdiff':'DX']
        return df2


    def SuperTrend(self,df, period=supertrend_period, multiplier=supertrend_multiplier, ohlc=['open', 'high', 'low', 'close']):
        """
        Function to compute SuperTrend
        Args :
            df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
            period : Integer indicates the period of computation in terms of number of candles
            multiplier : Integer indicates value to multiply the ATR
            ohlc: List defining OHLC Column names (default ['Open', 'High', 'low', 'Close'])
        Returns :
            df : Pandas DataFrame with new columns added for
                True Range (TR), ATR (ATR_$period)
                SuperTrend (ST_$period_$multiplier)
                SuperTrend Direction (STX_$period_$multiplier)
        """

        self.ATR(df, period, ohlc=ohlc)
        atr = 'ATR_' + str(period)
        st = 'ST'  # + str(period) + '_' + str(multiplier)
        stx = 'STX'  # + str(period) + '_' + str(multiplier)

        """
        SuperTrend Algorithm :
            BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
            BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
            FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                                THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
            FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND))
                                THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
            SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                            Current FINAL UPPERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                    Current FINAL LOWERBAND
                                ELSE
                                    IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                        Current FINAL UPPERBAND
        """

        # Compute basic upper and lower bands
        df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
        df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

        # Compute final upper and lower bands
        df['final_ub'] = 0.00
        df['final_lb'] = 0.00
        for i in range(period, len(df)):
            df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or \
                df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else \
                df['final_ub'].iat[i - 1]
            df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or \
                df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else \
                df['final_lb'].iat[i - 1]

        # Set the Supertrend value
        df[st] = 0.00
        for i in range(period, len(df)):
            df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[
                i] <= df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > \
                df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= \
                df['final_lb'].iat[i] else \
                df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] < \
                df['final_lb'].iat[i] else 0.00

            # Mark the trend direction up/down
        df[stx] = np.where((df[st] > 0.00), np.where(
            (df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)

        # Remove basic and final bands from the columns
        df.drop(['basic_ub', 'basic_lb', 'final_ub',
                'final_lb'], inplace=True, axis=1)

        df.fillna(0, inplace=True)
        return df
