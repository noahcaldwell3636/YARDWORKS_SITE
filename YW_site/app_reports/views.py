from django.shortcuts import render
from app_reports.models import Invoice, Company, CompanyGroup, EstablishedSite
import datetime
import simplejson

# Create your views here  

def render_report(request):
    # get report name
    report = request.get_full_path().split("/")[-1]
    if report == "Company Wide":
        return render_company_wide_sales(request, 'ReportPage.html')
    elif report == "DeliveryMap":
        return render_delivery_map(request, "DeliveryMap.html")
    else:
        return render_sales_report(request, "ReportPage.html")


def render_company_wide_sales(request, html_template):
    return render(request, html_template, {
            'company': 'All Companies', # WARNING: WILL RETURN A STRING WHEN THE REPORT IS FOR ALL COMPANIES WHICH MAY CAUSE ISSUES IF ANY COMPNAY FEILDs ARE ATTEMPTED TO BE REFERENCED IN THE HTML TEMPLATE
            'data': get_monthly_totals(Invoice.objects.all()),
            'data_json': simplejson.dumps(get_monthly_totals(Invoice.objects.all())),
            'companies': Company.objects.all(),
            'group_name': "AllCompanies",
            'groups': CompanyGroup.objects.all().values_list('name', flat=True),
            'type': 'sales',
        })

def render_sales_report(request, html_template):
    # set default group in case of invalid url
    default_group = "JimsCustomers"
    # get the correct group object
    group_name = request.get_full_path().split("/")[-2]
    # set group to a default if cant find group
    groups_query = CompanyGroup.objects.all()
    all_groups = CompanyGroup.objects.all().values_list('name', flat=True)
    # get group model object
    print(group_name)
    try:
        group = CompanyGroup.objects.get(name=group_name)
    except Exception as e: # default group if group from url isn't valid
        group = CompanyGroup.objects.get(name=default_group)
        print(group)
    # get companies within the group for the report
    companies = group.companies.all()
    print(companies)
    # get company name from URL, reverses the "format_name_for_url" custom template method to return the normal company
    # name before it was modified to be put in the url
    company_name = request.get_full_path().split("/")[-1].replace("-", " ").replace("(slash)", "/")
    print()
    print()
    print()
    print(company_name)
    print()
    print()
    print()

    if company_name == 'All Companies':
        company = 'All Companies for ' + group_name
        invoices = get_all_companies_invoices(companies)
    elif company_name == 'default':
        company = companies.first()
        invoices = Invoice.objects.filter(company=company).order_by('date')
    else:
        # get model object/company by name
        company = companies.get(name=company_name)
        # order monthly sales objects by year then month for company
        invoices = Invoice.objects.filter(company=company).order_by('date')

    # convert monthly data to a list of list for google chart
    monthly_totals = get_monthly_totals(invoices)
    # convert data to json so it can be passed to javascript/google charts
    data_json = simplejson.dumps(monthly_totals)
    # render html with tag data
    return render(request, html_template, {
        'company':company, # WARNING: WILL RETURN A STRING WHEN THE REPORT IS FOR ALL COMPANIES WHICH MAY CAUSE ISSUES IF ANY COMPNAY FEILDs ARE ATTEMPTED TO BE REFERENCED IN THE HTML TEMPLATE
        'data': monthly_totals,
        'data_json': data_json,
        'companies': companies,
        'group_name': group_name,
        'groups': all_groups,
        'type': 'sales'
    })



def render_delivery_map(request, html_template):
    sites = EstablishedSite.objects.all()

    # create list of lists of site data
    site_data = []
    for site in sites:
        name = site.name
        longitude = site.longitude
        latitude = site.latitude
        site_data.append([name, latitude, longitude])
    return render(request, html_template, {'site_data': site_data})



############################ HELPER METHODS ################################

def get_monthly_totals(invoices):
    """
    Methods takes queryset of invoices and outputs the totals of those
    invoices by month, in chronological order, in a list of lists that can be
    easily converted to json format (using simplejson.dump) for google charts.

    @param QuerySet invoices -  A query set of one or more objects of type 'Invoice' which is 
                                defined in this project in the app_reports. models file.

    Output format:
    [
        [Month, Sales],
        [{month/year string}, {monthly_sales_value float}],
        [{month/year string}, {monthly_sales_value float}],
        [{month/year string}, {monthly_sales_value float}],
        ...
    ]
    """
    monthly_totals = []
    beginning_year = 2015 # int(str(invoices.first().date).split("-")[0])
    beginning_month = 1 # int(str(invoices.first().date).split("-")[1])
    current_year, current_month = (datetime.datetime.now().year, datetime.datetime.now().month)
    for year in range(beginning_year, current_year+1):
        # if outputtiing for current year, only output up to current month
        if year == current_year:
            for month in range(1, current_month+1):
                monthly_totals.append(total_sales_for_month(invoices, year, month))
        # if outputting in a previous year, output all twelve months
        else:
            for month in range(1, 12+1):
                monthly_totals.append(total_sales_for_month(invoices, year, month))
    # insert headers
    monthly_totals.insert(0, ['Month', 'Sales'])
    return monthly_totals


def total_sales_for_month(invoices, year, month):
    """
    Sums the total sales amount for the given year and month out of the given queryset of invoices.
    Rounded to the nearest second decimal.

    @param QuerySet invoices -  A query set of one or more objects of type 'Invoice' which is 
                                defined in this project in the app_reports.models file.
    @param int year -           The year the invoice total will be calculated.
    @param in month -           The month the invoice total will be calculated.

    Output example:
    ['Jul 2018', 2899.50]
    """
    # get list of all the invoice (no tax) amounts
    inv_amounts = list(invoices.filter(date__year=year).filter(date__month=month).values_list("amount_without_tax", flat=True))
    # get rounded sum
    month_total = round(sum(inv_amounts), 2)
    month_date_str = datetime.datetime(year, month, 1).strftime('%b') + "-" + str(year) # day param are irrelevent
    return [month_date_str, month_total]


def get_all_companies_invoices(companies):
    """
    Returns a query set of all the invoices for each company given in the parameter.

    @param QuerySet companies - all the companies you wish to retrieve invoices for
    """
    accounts = []
    for account in companies.values_list('account', flat=True):
        accounts.append(account)
    return Invoice.objects.filter(customer_number__in=accounts).order_by('date')



########## NOT USED #######################################
def get_company_from_url(request, group_name, companies):
    """
    Retrieves the company model object based on the last URL subdirectory.

    WARNING: THIS METHOD WILL RETURN A STRING IN THE CASE OF THE URL BEING 'All-Companies', THIS 
    MAY CAUSE A ERROR IF ONE OF THE COMPANY'S FIELDS IS REFERENCED IN THE HTML TEMPLATE.

    @param django.core.handlers.wsgi.WSGIRequest request - request param that django set value for in all view methods
    @param str group_name -     the group that the report is for, used when creating the string for 'all companies
    @param QuerySet companies - the companies that are apart of the group for the report

    @returns report.models.Company or string 
    """
    # reverses the "format_name_for_url" custom template method to get the normal company instead of the string 
    # configured to be placed in the URL
    account = request.get_full_path().split("/")[-1].replace("-", " ").replace("(slash)", "/")
    if account == 'All Companies':
        company = 'All Companies for ' + group_name # sets company to a string for html display (WARNING)
    elif account == 'default':
        company = companies.first()
    else:
        company = companies.get(account=account)
    return company


def get_company_invoices_from_url(request, companies, company):
    """
    Retrieves the company model object based on the last URL subdirectory.

    WARNING: THIS METHOD WILL RETURN A STRING IN THE CASE OF THE URL BEING 'All-Companies', THIS 
    MAY CAUSE A ERROR IF ONE OF THE COMPANY'S FIELDS IS REFERENCED IN THE HTML TEMPLATE.

    @param django.core.handlers.wsgi.WSGIRequest request - request param that django set value for in all view methods
    @param QuerySet companies -     the companies that are apart of the group for the report
    @param Report.model.Company -   the company you wish to retrieve invoices from

    @returns QuerySet of report.models.Invoice
    """
    # get company name from URL
    account = request.get_full_path().split("/")[-1].replace("-", " ").replace("(slash)", "/")
    if account == 'All Companies':
        invoices = get_all_companies_invoices(companies)
    elif account == 'default':
        invoices = Invoice.objects.filter(company=company).order_by('date')
    else:
        # order monthly sales objects by year then month for company
        invoices = Invoice.objects.filter(company=company).order_by('date')
    return invoices
    