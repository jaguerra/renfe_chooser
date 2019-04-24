from trip_dates import *
from functools import reduce


class CandidateTicket:
    def __init__(self, name, valid_for_days, cost, num_trips):
        self.name = name
        self.valid_for_days = valid_for_days
        self.cost = cost
        self.num_trips = num_trips


candidate_tickets = [
    CandidateTicket("return", 1, 53.4, 2),
    CandidateTicket("abono 10", 8, 143.50, 10),
    CandidateTicket("abono 30", 30, 500.5, 30)
]


class SolutionNode:
    def __init__(self, start_date: date, end_date: date, candidate_ticket:CandidateTicket):
        self.start_date = start_date
        self.end_date = end_date
        self.candidate_ticket = candidate_ticket


class Solution:
    def __init__(self, total_cost:float, solution_nodes:list):
        self.total_cost = total_cost
        self.solution_nodes = solution_nodes


excluded_dates = [
    "2019-04-18",
    "2019-04-22",
    "2019-05-01",
    "2019-05-02",
    "2019-05-02",
    "2019-05-15",
    "2019-06-20",
    "2019-08-19",
    "2019-08-20",
    "2019-08-21",
    "2019-08-22",
    "2019-08-26",
    "2019-08-27",
    "2019-08-28",
    "2019-08-29",
]

trip_dates = generate_trip_dates(
    date.fromisoformat("2019-01-01"),
    date.fromisoformat("2019-12-31"),
    [1, 2, 3, 4],
    excluded_dates_from_iso_array(excluded_dates)
)



class Backtrack:
    def __init__(self, trip_dates:list, candidate_tickets:list):
        self.trip_dates = sorted(trip_dates)
        self.candidate_tickets = candidate_tickets
        self.solutions = []

    def analyse(self):
        self.backtrack([])
        print("Found {} solutions".format(len(self.solutions)))
        solutions = sorted(self.solutions, key=Solution.total_cost, reverse=True)
        for solution in solutions[:5]:
            print("Solution cost: {}".format(solution.total_cost))

    def backtrack(self, partial_solutions:list):
        if self.is_a_solution(partial_solutions):
            self.process_solution(partial_solutions)
        else:
            candidates = self.construct_candidates(partial_solutions)
            for candidate in candidates:
                partial_solutions.append(candidate)
                self.backtrack(partial_solutions)
                partial_solutions.pop()

    def is_a_solution(self, partial_solutions:list):
        if len(partial_solutions) == 0:
            return False
        return self.trip_dates[-1] <= partial_solutions[-1].end_date

    def process_solution(self, partial_solutions:list):
        total_cost = reduce((lambda x,y: x + y), map((lambda x: x.candidate_ticket.cost), partial_solutions))
        self.solutions.append(Solution(total_cost, partial_solutions[:]))

    def construct_candidates(self, partial_solutions:list):
        candidates = []
        for candidate_ticket in self.candidate_tickets:
            if len(partial_solutions) == 0:
                next_available_date = self.get_next_available_date(False)
            else:
                next_available_date = self.get_next_available_date(partial_solutions[-1].end_date)
            start_date = end_date = next_available_date
            trips_left = candidate_ticket.num_trips
            while trips_left > 0:
                trips_left -= 2
                end_date = next_available_date
                next_available_date = self.get_next_available_date(next_available_date)
                if next_available_date == False:
                    break
                if (next_available_date - start_date).days > candidate_ticket.valid_for_days:
                    break
            candidates.append(SolutionNode(start_date, end_date, candidate_ticket))

        return candidates

    def get_next_available_date(self, last_used_date):
        if last_used_date is False:
            return self.trip_dates[0]
        last_used_date_index = self.trip_dates.index(last_used_date)
        if len(self.trip_dates) <= last_used_date_index + 1:
            return False
        return self.trip_dates[last_used_date_index + 1]


Backtrack(trip_dates, candidate_tickets).analyse()
