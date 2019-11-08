from backtrack import CandidateTicket, Backtrack
from trip_dates import *

candidate_tickets = [
    CandidateTicket("abono 10", 8, 143.50, 10),
    CandidateTicket("abono 10 45", 45, 223.40, 10),
    CandidateTicket("abono 30", 30, 500.5, 30),
    CandidateTicket("abono 32", 30, 515.6, 32),
    CandidateTicket("abono 34", 30, 531.9, 34),
    CandidateTicket("abono 36", 30, 547.5, 36),
    CandidateTicket("abono 38", 30, 562.7, 38),
    CandidateTicket("abono 40", 30, 578.9, 40),
    CandidateTicket("abono 50", 30, 656.6, 50),
    CandidateTicket("return", 1, 57.4, 2)
]

excluded_dates = [
    "2019-01-01",
    "2019-01-07",
    "2019-03-01",
    "2019-03-04",
    "2019-03-05",
    "2019-04-15",
    "2019-04-16",
    "2019-04-17",
    "2019-04-18",
    "2019-04-22",
    "2019-05-01",
    "2019-05-02",
    "2019-05-03",
    "2019-05-10",
    "2019-05-15",
    "2019-06-20",
    "2019-06-21",
    "2019-07-12",
    "2019-07-15",
    "2019-08-19",
    "2019-08-20",
    "2019-08-21",
    "2019-08-22",
    "2019-08-26",
    "2019-08-27",
    "2019-08-28",
    "2019-08-29",
    "2019-12-26",
    "2019-12-30",
    "2019-12-31",
]

trip_dates = generate_trip_dates(
    date.fromisoformat("2019-01-01"),
    date.fromisoformat("2019-12-31"),
    [1, 2, 3, 4],
    excluded_dates_from_iso_array(excluded_dates)
)

trip_dates_2 = generate_trip_dates(
    date.fromisoformat("2019-01-01"),
    date.fromisoformat("2019-12-31"),
    [1, 2, 4],
    excluded_dates_from_iso_array(excluded_dates)
)

trip_dates_3 = generate_trip_dates(
    date.fromisoformat("2019-01-01"),
    date.fromisoformat("2019-12-31"),
    [2, 4],
    excluded_dates_from_iso_array(excluded_dates)
)

trip_dates_4 = generate_trip_dates(
    date.fromisoformat("2019-01-01"),
    date.fromisoformat("2019-12-31"),
    [2],
    excluded_dates_from_iso_array(excluded_dates)
)



print("Set #1 (4 days)")
Backtrack(trip_dates, candidate_tickets).analyse()
print("Set #2 (3 days)")
Backtrack(trip_dates_2, candidate_tickets).analyse()
print("Set #3 (2 days)")
Backtrack(trip_dates_3, candidate_tickets).analyse()
print("Set #4 (1 days)")
Backtrack(trip_dates_4, candidate_tickets).analyse()
