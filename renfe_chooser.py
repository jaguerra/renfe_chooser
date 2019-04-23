from trip_dates import *


class CandidateTicket:
    def __init__(self, name, valid_for_days, cost):
        self.name = name
        self.valid_for_days = valid_for_days
        self.cost = cost


candidate_tickets = [
    CandidateTicket("return", 1, 53.4),
    CandidateTicket("abono 10", 8, 143.50),
    CandidateTicket("abono 30", 30, 500.5)
]


class SolutionNode:
    def __init__(self, start_date: date, end_date: date, candidate_ticket:CandidateTicket):
        self.start_date = start_date
        self.end_date = end_date
        self.candidate_ticket = candidate_ticket


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
    def __init__(self, trip_dates, candidate_tickets):
        self.trip_dates = trip_dates
        self.candidate_tickets = candidate_tickets

    def backtrack(self, partial_solutions, k):
        if self.is_a_solution(partial_solutions, k):
            self.process_solution(partial_solutions, k)
        else:
            k += 1
            candidates = self.construct_candidates(partial_solutions, k)

    def is_a_solution(self, partial_solutions, k):
        return False

    def process_solution(self, partial_solutions, k):
        return

    def construct_candidates(self, partial_solutions, k):
        return []

