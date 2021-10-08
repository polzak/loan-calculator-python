import math
import argparse


PRINCIPAL = 0
PERIODS = 0
INTEREST = 0
PAYMENT = 0

HAS_PRINCIPAL = False
HAS_PERIODS = False
HAS_INTEREST = False
HAS_PAYMENT = False

INCORRECT_PARAMETERS = "Incorrect parameters"


def get_nominal_interest(percentage):
    return percentage / 12 / 100

def get_number_of_payments(P, A, i):
    denominator = A - i * P
    if denominator == 0:
        print("Cannot get the number of payments because of zero denominator.")
        return 0
    else:
        return math.ceil(math.log(A / denominator, 1 + i))

def print_readable_months(m):
    year = 0
    month = 0
    template = "It will take {} to repay this loan!"
    p = "" #8 years and 2 months
    year = m // 12
    month = m % 12
    year_part = ""
    month_part = ""
    if year == 1:
        year_part = "1 year"
    elif year > 1:
        year_part = "{} years".format(year)
    if month == 1:
        month_part = "1 month"
    elif month > 1:
        month_part = "{} months".format(month)
    if year > 0 and month > 0:
        p = year_part + " and " + month_part
    else:
        p = year_part + month_part
    print(template.format(p))

def get_annuity_payment(P, n, i):
    pow_value = math.pow(1 + i, n)
    numerator = i * pow_value
    denominator = pow_value - 1
    if denominator == 0:
        print("Cannot get the annuity payment because of zero denominator.")
        return 0
    else:
        return math.ceil(P * numerator / denominator)

def get_principal(A, n, i):
    pow_value = math.pow(1 + i, n)
    numerator = i * pow_value
    denominator = pow_value - 1
    if denominator == 0:
        print("Cannot get the annuity payment because of zero denominator.")
        return 0
    big_denominator = numerator / denominator
    if big_denominator == 0:
        print("Cannot get the annuity payment because of zero big denominator.")
        return 0
    return math.floor(A / big_denominator)



def compute_annuity():
    option = ""
    if not HAS_PRINCIPAL:
        option = "p"
    elif not HAS_PAYMENT:
        option = "a"
    elif not HAS_PERIODS:
        option = "n"
    principal = PRINCIPAL
    monthly_payment = PAYMENT
    interest = INTEREST
    periods = PERIODS
    if option == "n":
        #get nominal interest
        i = get_nominal_interest(interest)
        periods = get_number_of_payments(principal, monthly_payment, i)
        print_readable_months(periods)
    elif option == "a":
        #get nominal interest
        i = get_nominal_interest(interest)
        monthly_payment = get_annuity_payment(principal, periods, i)
        print("Your annuity payment = {}!".format(monthly_payment))
    elif option == "p":
        #get nominal interest
        i = get_nominal_interest(interest)
        principal = get_principal(monthly_payment, periods, i)
        print("Your loan principal = {}!".format(principal))
    over_payment = monthly_payment * periods - principal
    print("Overpayment = {}".format(int(over_payment)))


def compute_diff():
    total_payment = 0
    principal = PRINCIPAL
    periods = PERIODS
    interest = INTEREST
    i = get_nominal_interest(interest)
    for m in range(1, periods + 1):
        d = math.ceil(principal / periods + i * (principal - principal * (m - 1) / periods))
        total_payment += d
        print("Month {}: payment is {}".format(m, d))
    over_payment = total_payment - principal
    print("Overpayment = {}".format(int(over_payment)))


def loan_calculator():
    global PRINCIPAL, PERIODS, INTEREST, PAYMENT
    global HAS_PRINCIPAL, HAS_PERIODS, HAS_INTEREST, HAS_PAYMENT
    argument_count = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--principal")
    parser.add_argument("--periods")
    parser.add_argument("--interest")
    parser.add_argument("--payment")
    args = parser.parse_args()
    if args.interest:
        INTEREST = float(args.interest)
        HAS_INTEREST = True
        argument_count += 1
    else:
        print(INCORRECT_PARAMETERS)
        return
    if args.principal:
        PRINCIPAL = float(args.principal)
        HAS_PRINCIPAL = True
        argument_count += 1
    if args.periods:
        PERIODS = int(args.periods)
        HAS_PERIODS = True
        argument_count += 1
    if args.payment:
        PAYMENT = float(args.payment)
        HAS_PAYMENT = True
        argument_count += 1
    if argument_count < 3:
        print(INCORRECT_PARAMETERS)
        return
    if INTEREST < 0 or PRINCIPAL < 0 or PERIODS < 0 or PAYMENT < 0:
        print(INCORRECT_PARAMETERS)
        return
    if args.type == "annuity":
        compute_annuity()
    elif args.type == "diff" and not HAS_PAYMENT:
        compute_diff()
    else:
        print(INCORRECT_PARAMETERS)


loan_calculator()


