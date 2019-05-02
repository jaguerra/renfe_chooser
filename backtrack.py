from functools import reduce
from datetime import date


class CandidateTicket:
    def __init__(self, name, valid_for_days, cost, num_trips):
        self.name = name
        self.valid_for_days = valid_for_days
        self.cost = cost
        self.num_trips = num_trips


class SolutionNode:
    def __init__(self, start_date: date, end_date: date, candidate_ticket:CandidateTicket, wasted_tickets:int, ticket_dates:list):
        self.start_date = start_date
        self.end_date = end_date
        self.candidate_ticket = candidate_ticket
        self.wasted_tickets = wasted_tickets
        self.ticket_dates = ticket_dates


class Solution:
    def __init__(self, total_cost:float, solution_nodes:list):
        self.total_cost = total_cost
        self.solution_nodes = solution_nodes

    def get_aggregated_tickets(self):
        aggregation = {}
        for solution_node in self.solution_nodes:
            key = solution_node.candidate_ticket.name
            if key in aggregation:
                aggregation[key] += 1
            else:
                aggregation[key] = 1
        return aggregation

    def get_wasted_tickets(self):
        return reduce((lambda x, y: x + y), map(lambda x: x.wasted_tickets, self.solution_nodes))


class Backtrack:
    def __init__(self, trip_dates:list, candidate_tickets:list):
        self.trip_dates = sorted(trip_dates)
        self.candidate_tickets = candidate_tickets
        self.solutions = []
        self.partial_cost_by_date = {}

    def analyse(self):
        self.backtrack([])
        print("Found {} solutions".format(len(self.solutions)))
        solutions = sorted(self.solutions, key=lambda item:item.total_cost)
        for solution in solutions[:5]:
            print("Solution cost: {} {}. Wasted tickets: {}".format(solution.total_cost, solution.get_aggregated_tickets(), solution.get_wasted_tickets()))
        return

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
        total_cost = self.get_solution_cost(partial_solutions)
        self.solutions.append(Solution(total_cost, partial_solutions[:]))
        if len(self.solutions) % 10000 == 0:
            print('.', end='', flush=True)

    def get_solution_cost(self, partial_solutions:list):
        if len(partial_solutions):
            return reduce((lambda x,y: x + y), map((lambda x: x.candidate_ticket.cost), partial_solutions))
        else:
            return 0

    def is_better_than_partial_solution(self, solution_date, cost):
        if solution_date in self.partial_cost_by_date:
            if cost < self.partial_cost_by_date[solution_date]:
                self.partial_cost_by_date[solution_date] = cost
                return True
            else:
                return False
        else:
            self.partial_cost_by_date[solution_date] = cost
            return True

    def construct_candidates(self, partial_solutions:list):
        candidates = []
        current_cost = self.get_solution_cost(partial_solutions)
        for candidate_ticket in self.candidate_tickets:
            ticket_dates = []
            if len(partial_solutions) == 0:
                next_available_date = self.get_next_available_date(False)
            else:
                next_available_date = self.get_next_available_date(partial_solutions[-1].end_date)
            start_date = end_date = next_available_date
            trips_left = candidate_ticket.num_trips
            while trips_left > 0:
                trips_left -= 2
                end_date = next_available_date
                ticket_dates.append(next_available_date)
                next_available_date = self.get_next_available_date(next_available_date)
                if next_available_date == False:
                    break
                if (next_available_date - start_date).days > candidate_ticket.valid_for_days:
                    break

            if self.is_better_than_partial_solution(end_date, current_cost + candidate_ticket.cost):
                candidates.append(SolutionNode(start_date, end_date, candidate_ticket, trips_left, ticket_dates))

        return candidates

    def get_next_available_date(self, last_used_date):
        if last_used_date is False:
            return self.trip_dates[0]
        last_used_date_index = self.trip_dates.index(last_used_date)
        if len(self.trip_dates) <= last_used_date_index + 1:
            return False
        return self.trip_dates[last_used_date_index + 1]
