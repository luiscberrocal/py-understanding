from decimal import Decimal, getcontext

# Set precision for financial calculations
getcontext().prec = 20


def anual_tax(monthly_salary: Decimal, deductions: Decimal) -> Decimal:
    """
    Calculates the expected annual Impuesto sobre la Renta (income tax) for a
    Panamanian natural person.

    This function is based on the Panamanian tax law for a single taxpayer.
    It takes into account the following assumptions based on standard accounting
    practices:
    1. The "décimo tercer mes" (13th-month salary) is a mandatory bonus equal
       to one month's salary and is considered tax-exempt for income tax purposes.
    2. The annual taxable income is based on the sum of 12 months' salaries.
    3. The calculation uses the progressive tax brackets applicable to individuals.

    Args:
        monthly_salary (Decimal): The gross monthly salary.
        deductions (Decimal): The total annual deductions to be applied to
                              the taxable income base.

    Returns:
        Decimal: The total annual income tax payment due.
    """
    if not isinstance(monthly_salary, Decimal) or not isinstance(deductions, Decimal):
        raise TypeError("Both monthly_salary and deductions must be of type Decimal.")

    # Calculate the annual taxable income base.
    # The 13th month is generally tax-exempt, so we only use 12 months for the taxable base.
    taxable_base = (monthly_salary * Decimal('12')) - deductions

    # Ensure taxable income is not negative
    if taxable_base < Decimal('0'):
        taxable_base = Decimal('0')

    # Define the tax brackets and rates in Panamanian Balboas (B/.)
    tax_brackets = [
        (Decimal('11000.00'), Decimal('0.00')),
        (Decimal('50000.00'), Decimal('0.15')),
        (None, Decimal('0.25'))  # The last bracket is for everything above 50,000
    ]

    total_tax = Decimal('0')

    # Apply the progressive tax rates
    # Bracket 1: up to 11,000
    if taxable_base <= tax_brackets[0][0]:
        total_tax = Decimal('0')

    # Bracket 2: excess over 11,000 up to 50,000
    elif taxable_base <= tax_brackets[1][0]:
        base_over_first_bracket = taxable_base - tax_brackets[0][0]
        total_tax = base_over_first_bracket * tax_brackets[1][1]

    # Bracket 3: excess over 50,000
    else:
        # Tax on the second bracket (from 11,000 to 50,000)
        tax_on_second_bracket = (tax_brackets[1][0] - tax_brackets[0][0]) * tax_brackets[1][1]

        # Tax on the remaining income
        base_over_second_bracket = taxable_base - tax_brackets[1][0]
        tax_on_remaining = base_over_second_bracket * tax_brackets[2][1]

        total_tax = tax_on_second_bracket + tax_on_remaining

    return total_tax.quantize(Decimal('0.01'))


if __name__ == "__main__":
    # Example usage
    # Scenario 1: Salary of B/. 1,500 per month with no deductions
    salary_1 = Decimal('1500')
    deductions_1 = Decimal('0')
    tax_1 = anual_tax(salary_1, deductions_1)
    print(f"Scenario 1: Monthly salary B/. {salary_1}, Deductions B/. {deductions_1}")
    print(f"Annual Taxable Base: B/. {(salary_1 * Decimal('12')) - deductions_1}")
    print(f"Annual Tax Due: B/. {tax_1}\n")

    # Scenario 2: Salary of B/. 5,000 per month with B/. 2,000 in deductions
    salary_2 = Decimal('5000')
    deductions_2 = Decimal('2000')
    tax_2 = anual_tax(salary_2, deductions_2)
    print(f"Scenario 2: Monthly salary B/. {salary_2}, Deductions B/. {deductions_2}")
    print(f"Annual Taxable Base: B/. {(salary_2 * Decimal('12')) - deductions_2}")
    print(f"Annual Tax Due: B/. {tax_2}\n")

    # Scenario 3: Salary of B/. 8,000 per month with B/. 5,000 in deductions
    salary_3 = Decimal('8000')
    deductions_3 = Decimal('5000')
    tax_3 = anual_tax(salary_3, deductions_3)
    print(f"Scenario 3: Monthly salary B/. {salary_3}, Deductions B/. {deductions_3}")
    print(f"Annual Taxable Base: B/. {(salary_3 * Decimal('12')) - deductions_3}")
    print(f"Annual Tax Due: B/. {tax_3}")
