from time import strptime


class MovieList:

    def __init__(self, movies, data_format):
        self.movies = movies
        self.data_format = data_format
        """for simplicity make each month 31 day ( wrong day value will be -1, -1, -1)"""
        self.day_star_end = [[-1, -1, -1]] * 372 # field movie, start day , end day
        self.__update()
        self.final_list = []
        self.max_profit()

    @staticmethod
    def _day(date):
        if len(date) == 2:
            day, month = date
            day = int(day)
            month = strptime(month, '%b').tm_mon
            t = day + 31 * (month-1) - 1
            return t
        else:
            print('data format error', date)
            return None

    def __update(self):

        for (mv, star_day, end_day) in self.movies:
            t1, t2 = self._day(star_day.split()), self._day(end_day.split())
            print(t1,t2)
            if (t1 == -1) or (t2 == -1):
                break
            """ offer start same day : total day less more space for other offer """
            pre_inter = (self.day_star_end[t1][1] - self.day_star_end[t1][2])
            if self.day_star_end[t1][1] != -1:
                if (t2 - t1) < pre_inter:
                    self.day_star_end[t1] = [mv, t1, t2]
            else:
                self.day_star_end[t1] = [mv, t1, t2]

    def max_profit(self, ):
        prev_mv, pre_start, pre_end = -1, -1, -1
        for pos, (values) in enumerate(self.day_star_end):
            mv, cu_start, cu_end = values

            if (prev_mv == -1) and (mv == -1):
                """ no movie still check next day"""
                continue
            elif prev_mv == -1:
                """movie offer and no pending decision"""
                if cu_end == cu_start:
                    """ one day movie take it remove if any pending"""
                    self.final_list.append([mv, cu_start, cu_end])
                    prev_mv, pre_start, pre_end = -1, -1, -1
                else:
                    prev_mv, pre_start, pre_end = mv, cu_start, cu_end
            elif mv == -1:
                """ no new movie today check if pre end day reach"""
                if pos > pre_end:
                    self.final_list.append([prev_mv, pre_start, pre_end])
                    prev_mv, pre_start, pre_end = -1, -1, -1
            elif cu_end < pre_end:
                """ next movie offer date end early then  prev so replace else same"""
                prev_mv, pre_start, pre_end = mv, cu_start, cu_end

