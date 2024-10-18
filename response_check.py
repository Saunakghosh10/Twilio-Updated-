import time
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the Excel data
data = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")

# Remove the last row from the DataFrame
# data = data[:-1]

def match_vendors(client_row, top_n=3):
    client_requirements = client_row.get('Requirement Description', '')
    client_keywords = client_row.get('Requirement description Keywords', '')
    
    #print(client_requirements)
    client_text = f"{client_requirements} {client_keywords}".strip()
    print("The client row is -- ",client_row)
    print("The client row index  is----",client_row.index)
    
    client_index = client_row.name
    # if client_index not in data.index:
    #     raise ValueError(f"Client index {client_index} not found in data index: {data.index.tolist()}")    
    vendor_texts = data.drop(index=client_index)[['Requirement Description', 'Requirement description Keywords', 'Offering Keywords']].apply(
    lambda row: ' '.join(row.values.astype(str)), axis=1)
    
    
 
    top_matches = process.extract(client_text, vendor_texts, scorer=fuzz.token_set_ratio, limit=top_n)
    #print(top_matches)
    matched_vendors_str = []
    ai_recommendations = [] 
    for match_tuple in top_matches:
        best_match, score, vendor_index = match_tuple  # Unpack match, score, and index
        matched_vendor_row = data.iloc[vendor_index]
        
        # Check if the matched vendor row is a duplicate of the current row
        is_duplicate = (
            matched_vendor_row['Requirement Description'] == client_row['Requirement Description'] and
            matched_vendor_row['Requirement description Keywords'] == client_row['Requirement description Keywords'] and
            matched_vendor_row['Offering Keywords'] == client_row['Offering Keywords']
        )
        
        threshold = 50  # Adjust the threshold as needed
        if score >= threshold and not is_duplicate:
            print('index_number :',vendor_index)
            # Get the full details of the matched vendor
            # matched_vendor_row = data.iloc[vendor_index]  # Find the vendor row by index
            
            ai_recommendation = (
                f"*AI RECOMMENDATION !* \n"
                f"\033[1m{score}\033[0m % is *matching* with the below vendor .\n\n"
                f"I recommend you to speak with {matched_vendor_row['Name']} ({matched_vendor_row['LinkedIn']} ,{matched_vendor_row['Designation']} , {matched_vendor_row['Website']}).\n\n"
                #f"I’m {matched_vendor_row['Name']}, {matched_vendor_row['Designation']} at {matched_vendor_row['Company Name']}."
                f"Please find his offerings: {matched_vendor_row['Offerings']}.\n\n"
                f"{matched_vendor_row['Sales Pitch']}🚀.\n"
                #f"We’re open to collaborations and partnerships with VC partners, mentors, and angels to create a thriving community 🔗." 
            )
            matched_vendors_str.append(ai_recommendation)
              # Append the recommendation message
            #print(ai_recommendation)
    #print(len(matched_vendors_str))

  
     # Join the list into a comma-separated string or return a message if no match is found
    if matched_vendors_str:
        # Return the first AI recommendation and matched vendors as a comma-separated string
        return  matched_vendors_str

    else:
        return "No suitable vendor match found", None
    

# # Get the last row (before removal) to use as the client inpu
# last_row = data.iloc[-1]
# matched_vendors_str = match_vendors(last_row)

# # # Output the result
# print("Matched Vendor Data for the Last Client:")
# print(matched_vendors_str)