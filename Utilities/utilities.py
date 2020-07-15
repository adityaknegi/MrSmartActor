from time import strptime


months2days = {"Jan": 31, "Feb": 29, "Mar": 31, "Apr": 30, "May": 31, "Jun": 30, "Jul": 31, "Aug": 31
             , "Sep": 30, "Oct": 31, "Nov": 30, "Dec": 31}


days2months_date = []
months_date2days = {}

count =0
for month, days in months2days.items():

    for day in range(days):
        days2months_date.append(str(day+1) + ' ' + month)
        months_date2days[str(day+1) + month] = day + count
    count += months2days[month]

max_days = sum(months2days.values()) + 1


def find_day(date, reverse=False):
    if reverse:
        return days2months_date[date]
    else:
        if len(date) == 2:
            day, month = date
            day = str(int(day)) # 02 to 2
            str1 = day + month
            return months_date2days[str1]

    print('data format error', date)
    return -1


class MovieList:

    def __init__(self, movies, data_format):
        self.movies = movies
        self.data_format = data_format
        self.day_star_end = [[-1, -1, -1] for i in range(max_days)]  # field movie, start day , end day
        self.__update()
        self.final_list = []
        self.max_profit()

    def __update(self):

        for (mv, start_day, end_day) in self.movies:
            t1, t2 = find_day(start_day.split()), find_day(end_day.split())
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
                    self.final_list.append([mv, find_day(cu_start,reverse=True),
                                            find_day(cu_end, reverse=True)])
                else:
                    """ add to pending offers"""
                    prev_mv, pre_start, pre_end = mv, cu_start, cu_end
            elif mv == -1:
                """ no movie offer at current time check if pre end day reached"""
                if pos > pre_end:
                    self.final_list.append([prev_mv,
                                            find_day(pre_start, reverse=True),
                                            find_day(pre_end,reverse=True)]
                                           )
                    prev_mv, pre_start, pre_end = -1, -1, -1
            elif (pre_end != -1) and (cu_end != -1):
                """ if pending and current offers exits """
                if pos > pre_end:
                    """ check pending offer end date with with cur date if less save to final offers"""
                    self.final_list.append([prev_mv,
                                            find_day(pre_start,reverse=True),
                                            find_day(pre_end, reverse=True)]
                                           )
                    prev_mv, pre_start, pre_end = -1, -1, -1

                    """movie offer and no pending decision"""
                    if cu_end == cu_start:
                        """ if movie duration one day then add to final offers """
                        self.final_list.append([mv,
                                                find_day(cu_start,reverse=True),
                                                find_day(cu_end,reverse=True)]
                                               )
                    else:
                        prev_mv, pre_start, pre_end = mv, cu_start, cu_end
                else:
                    if cu_start == cu_end:
                        """ curr offer end day == start day  add to list remove pending"""
                        self.final_list.append([mv,
                                                find_day(cu_start,reverse=True),
                                                find_day(cu_end,reverse=True)]
                                               )
                        prev_mv, pre_start, pre_end = -1, -1, -1
                    elif cu_end < pre_end:
                        """ pending offer last day more then current day so replace """
                        prev_mv, pre_start, pre_end = mv, cu_start, cu_end


class MoviesListSET:
    """for simplicity make each month 31 day ( wrong day value will be -1, -1, -1)"""

    def __init__(self, movies, data_format, max_len):
        """ str to int 1 to 372 """
        self.movies = [[mv, find_day(start_day.split()), find_day(end_day.split())]
                       for (mv, start_day, end_day) in movies]

        self.data_format = data_format
        self.max_len = max_len
        self.day_star_end = [[] for i in range(max_days)]  # field movie, start day , end day
        self.final_movies_list = []
        self.heights = []

    def recursion(self, start, movies=None):
        """max depth then return"""
        if start > max_days-1:
            """ no of movies are max """
            if len(movies) == self.max_len:
                self.final_movies_list.append(movies)
            return

        """ make all possible outcome
          for n movies take any one or none 
          """
        """ one movie take"""
        for (mv, _, end_day) in self.day_star_end[start]:
            if movies == None:
                temp = []
            else:
                temp = movies.copy()

            temp.append((mv, find_day(start,reverse=True),
                         find_day(end_day, reverse=True)))
            """ if start and end day ame the add and check next day"""
            if start == end_day:
                self.recursion(end_day + 1, temp)
            else:
                """ check in end day  index"""
                self.recursion(end_day, temp)

        """
      
        no movie taken from this day 
        
        """
        if movies == None:
            movies = []
            self.recursion(start + 1, movies)
        else:
            self.recursion(start + 1, movies)

    def movies_list(self):

        """ add all movie at start day with name and end day"""

        for (mv, start_day, end_day) in self.movies:
            self.day_star_end[start_day].append([mv, start_day, end_day])
        self.recursion(0)
