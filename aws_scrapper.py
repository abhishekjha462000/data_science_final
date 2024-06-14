import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

def aws_maker(environment_html, cloud_html, region_html, html):
    
    # get all the environments @environment_html
    environment_soup = BeautifulSoup(environment_html, 'html.parser')
    environments = [tr.find_all('td')[0].text for tr in environment_soup.find_all('tr')]

    # get all the cloud environments @cloud_html
    cloud_soup = BeautifulSoup(cloud_html, 'html.parser')
    dirty_clouds = [tr.find_all('td')[0].text for tr in cloud_soup.find_all('tr')]

    clouds = []
    for name in dirty_clouds:
        if name.lower() == 'gst to be collected' or name.lower() == 'amazon web services india private limited' or name in environments:
            continue
        clouds.append(name)

    clouds = set(clouds) # now we have all the clouds

    # get all the regions @region_html
    region_soup = BeautifulSoup(region_html, 'html.parser')
    dirty_regions = [tr.find_all('td')[0].text for tr in region_soup.find_all('tr')]

    regions = []
    for name in diry_regions:
        if name in environments or name in clouds:
            continue
        if name.lower() == 'gst to be collected' or name.lower() == 'amazon web services india private limited':
            continue
        regions.append(name)

    regions = set(regions)

    soup = BeautifulSoup(html, 'html.parser')

    ALL_TRS = soup.find_all('tr')

    def tr_checker(tr):
        one, two, three = [td.text for td in tr.find_all('td')]

        return len(two) != 0
    
    VALID_TRS = list(filter(tr_checker, ALL_TRS))


    # make the initial dataframe
    billing_slab = []
    usage_quantity = []
    actual_bill_in_usd = []
    row_number = []
    
    for tr in VALID_TRS:
        one, two, three = [td.text for td in tr.find_all('td')]
        billing_slab.append(one)
        usage_quantity.append(two)
        actual_bill_in_usd.append(three)
        row_number.append(int(tr['aria-rowindex']))
    
    # print(actual_bill_in_usd)
    
    
    def actual_bill_transfomer(bill):
        bill = bill.replace('USD', '')[1::].replace(',', '')
        bill = float(bill)
        return bill
    
    actual_bill_in_usd = list(map(actual_bill_transfomer, actual_bill_in_usd))
        
    
    df = pd.DataFrame({
                        'billing_slab': billing_slab, 
                       'usage_quantity': usage_quantity, 
                       'actual_bill_in_usd': actual_bill_in_usd, 
                       'row_number': row_number
                      }
                     )



    # getting all the environment numbers
    ENVIRONMENT_TRS = list(filter(lambda x : x.find_all('td')[0].text in environments, ALL_TRS))
    environment_row_numbers = [int(tr['aria-rowindex']) for tr in ENVIRONMENT_TRS]
    
    def environment_decider(row_number):
        if row_number > environment_row_numbers[4]:
            return environments[4]
        elif row_number > environment_row_numbers[3]:
            return environments[3]
        elif row_number > environment_row_numbers[2]:
            return environments[2]
        elif row_number > environment_row_numbers[1]:
            return environments[1]
        else:
            return environments[0]


    df['environment'] =  df['row_number'].apply(environment_decider)

    billing_components = []
    
    for index,tr in enumerate(ALL_TRS):
        # find all the trs which have 3 valid data
        tds = tr.find_all('td')
    
        # this tr is a valid tr if the 1st td is non empty
        if len(tds[1].text) != 0:
            # find the tr which has tds[1] as 0
            # this tr is at the position index
            start = index
            
            while start >= 0:
                
                # we are at the tr which is at the position start
                if len(ALL_TRS[start].find_all('td')[1].text) == 0:
                    
                    billing_components.append(ALL_TRS[start].find_all('td')[0].text)
                    break
                    
                start = start-1

    df['billing_component'] = billing_components

    cloud_components = []

    for index,tr in enumerate(ALL_TRS):
        # find the tr which has 3 not blank td's 
        tds = tr.find_all('td')
    
        if len(tds[1].text) != 0: # this means that we are at the valid tr
            # now we need to find the cloud component of this 
            # for that just move backwards and find the string that matches a string in clouds simple as that
            start = index
    
            while start >= 0:
                # keep moving backwards until you find a tr whose 1st component is in clouds
                if ALL_TRS[start].find_all('td')[0].text in clouds:
                    cloud_components.append(ALL_TRS[start].find_all('td')[0].text)
                    break
                start = start - 1


    df['cloud_component'] = cloud_components

    region_col = []
    for index,tr in enumerate(ALL_TRS):
        # find the tr which has 3 non blank values
        tds = tr.find_all('td')
        # print(len(tds))
        # continue;
        # print(tds[1].text)
        # continue;
    
        if len(tds[1].text) != 0:
    
            # now you need to move backwards
            start = index
            
            while start >= 0:
                # find the tr which has only 2 non blank values and whose 0th values matches with a region
                if ALL_TRS[start].find_all('td')[0].text in regions:
                    region_col.append(ALL_TRS[start].find_all('td')[0].text)
                    break
                start = start - 1
    
    df['region'] = region_col

    mask = df['actual_bill_in_usd'] != 0
    df_1 = df[mask]
    
    columns = ['environment', 'cloud_component', 'region', 'billing_component', 'billing_slab', 'usage_quantity', 'actual_bill_in_usd']
    final = df_1[columns].reset_index(drop = True) # final dataframe

    def gst_checker(tr):
        one, two, three = [td.text for td in tr.find_all('td')]
        return one.lower() == 'gst to be collected'

    GST_TRS = list(filter(gst_checker, ALL_TRS))
    
    gsts = [float(tr.find_all('td')[2].text.replace('USD', '').replace(',', '')[1::]) for tr in GST_TRS]
    
    
    final_gsts = pd.DataFrame({'environment': environments, 'gst_in_usd':gsts})

    return final, final_gsts
