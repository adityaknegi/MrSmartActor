from time import strptime


class MovieList:

    def __init__(self, movies, data_format):
        self.movies = movies
        self.data_format = data_format
        """for simplicity make each month 31 day ( wrong day value will be -1, -1, -1)"""
        self.day_star_end = [[-1, -1, -1]] * 373 # field movie, start day , end day
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
            return -1

    def __update(self):

        for (mv, star_day, end_day) in self.movies:
            t1, t2 = self._day(star_day.split()), self._day(end_day.split())
            if (t1 == -1) or (t2 == -1):
                continue
            """ 
             if there are multiple offer on same day then take add offer whichever 
             has the shortest duration  
             """
            pre_dur = (self.day_star_end[t1][1] - self.day_star_end[t1][2])
            cur_dur = t2 - t1
            if self.day_star_end[t1][1] != -1:
                """ new offer has less duration take it"""
                if cur_dur < pre_dur:
                    self.day_star_end[t1] = [mv, t1, t2]
            else:
                self.day_star_end[t1] = [mv, t1, t2]

    def max_profit(self):
        """
        1.movie with start and end day same best always add to final list
        Algo start :
        0. loop
        case 1: if no offer (prev_m and cur_m) go to next index(0.loop) else go to next case
        case 2: three condition only prev_m or cur_m, both
        case 2.1: if only cur_m exits
                1. if curr offer end day == start day  add to final offer list
                and make prev null go to next index (0. loop) else save in pending offer (prev)
        case 2.2: if only prev_m exits
                1.  if  pending offer last day less then current day  save pending offer and make pending -1,
                go to next index(0. loop), else no change go to next index(0. loop)
        case 2.3: if both exits
                check pending offer last day less then current day
                if yes:
                    save pending offer(prev_m)  make prev (-1) go to next line
                    check cur_m
                        1. if curr offer end day == start day  add to final offer list
                        and  go to next index (0. loop) else save in pending offer (prev)
                if no:
                    if curr offer end day == start day  add to list  and make prev null go to next index
                    (0. loop) else next line
                    check if prev end day > cur end day
                        if yes:
                            replace prev with cur
                        else:
                            go to 0. loop
        ends:
        """
        prev_mv, pre_start, pre_end = -1, -1, -1
        for pos, (values) in enumerate(self.day_star_end):
            mv, cu_start, cu_end = values

            if (prev_mv == -1) and (mv == -1):
                """ no movie still check next day"""
                pass
            elif prev_mv == -1:
                """movie offer and no pending decision"""
                if cu_end == cu_start:
                    """ if movie duration one day then add to final offers """
                    self.final_list.append([mv, cu_start, cu_end])
                else:
                    """ add to pending offers"""
                    prev_mv, pre_start, pre_end = mv, cu_start, cu_end
            elif mv == -1:
                """ no movie offer at current time check if pre end day reached"""
                if pos > pre_end:
                    self.final_list.append([prev_mv, pre_start, pre_end])
                    prev_mv, pre_start, pre_end = -1, -1, -1
            elif (pre_end != -1) and (cu_end != -1):
                """ if pending and current offers exits """
                if pos > pre_end:
                    """ check pending offer end date with with cur date if less save to final offers"""
                    self.final_list.append([prev_mv, pre_start, pre_end])
                    prev_mv, pre_start, pre_end = -1, -1, -1

                    """movie offer and no pending decision"""
                    if cu_end == cu_start:
                        """ if movie duration one day then add to final offers """
                        self.final_list.append([mv, cu_start, cu_end])
                    else:
                        prev_mv, pre_start, pre_end = mv, cu_start, cu_end
                else:
                    if cu_start == cu_end:
                        """ one day movie take it remove if any pending"""
                        self.final_list.append([mv, cu_start, cu_end])
                        prev_mv, pre_start, pre_end = -1, -1, -1
                    elif cu_end < pre_end:
                        """ next movie offer date end early then  prev so replace else same"""
                        prev_mv, pre_start, pre_end = mv, cu_start, cu_end
