import json
import re
import pandas as pd

def parse_elite16_data():
    """
    Parse JSON data from standings_script_105.js to extract comprehensive
    Elite 16 standings for all case study teams
    """
    
    print("Parsing Elite 16 JSON data from script file...")
    print("=" * 80)
    
    # Read the JavaScript file
    with open('standings_script_105.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON data - it's after "49:[" and before the closing
    # Find the JSON structure
    json_match = re.search(r'49:\[(.*)\]', content, re.DOTALL)
    
    if not json_match:
        print("✗ Could not find JSON data")
        return None
    
    json_str = json_match.group(1)
    
    # Clean up the JSON string - it's escaped
    # Remove self.__next_f.push([1," prefix
    json_str = json_str.replace('self.__next_f.push([1,"', '')
    
    # The data structure is complex - let's parse it step by step
    try:
        # Extract the games array
        games_match = re.search(r'"games":\[(.*?)\],"standings"', json_str, re.DOTALL)
        
        if games_match:
            games_data = '[' + games_match.group(1) + ']'
            
            # Try to parse as JSON
            # This is tricky because of nested structures
            print("Found games data, parsing...")
            
            # Extract standings data instead - more useful
            standings_match = re.search(r'"standings":\[(.*?)\]', json_str, re.DOTALL)
            
            if standings_match:
                print("✓ Found standings data!")
                standings_str = '[' + standings_match.group(1) + ']'
                
                # Parse standings JSON
                try:
                    standings_data = json.loads(standings_str)
                    print(f"✓ Parsed {len(standings_data)} standing records")
                    
                    # Process standings
                    all_standings = []
                    
                    for standing in standings_data:
                        record = {
                            'Group': standing.get('groupPairingCode', 'N/A'),
                            'Rank': standing.get('rank', 'N/A'),
                            'Team_Code': standing.get('code', 'N/A'),
                            'Team_Name': standing.get('officialName', 'N/A'),
                            'Team_Short_Name': standing.get('shortName', 'N/A'),
                            'GP': standing.get('gamesPlayed', 0),
                            'W': standing.get('wins', 0),
                            'L': standing.get('losses', 0),
                            'PF': standing.get('pointsFor', 0),
                            'PA': standing.get('pointsAgainst', 0),
                            'PD': standing.get('pointsDifference', 0),
                            'PTS': standing.get('points', 0),
                            'Qualified': standing.get('isQualified', False)
                        }
                        all_standings.append(record)
                    
                    df = pd.DataFrame(all_standings)
                    
                    # Sort by Group and Rank
                    df = df.sort_values(['Group', 'Rank'])
                    
                    print("\n" + "=" * 80)
                    print("COMPLETE ELITE 16 STANDINGS")
                    print("=" * 80)
                    print(df.to_string(index=False))
                    
                    # Filter case study teams
                    case_study_codes = ['NCT', 'NAM', 'JOH', 'FBE', 'MMA', 'DAR', 'BHB']
                    
                    # Try different code variations
                    case_study_codes_variations = {
                        'NCT': ['NCT', 'NTE'],  # Nairobi City Thunder / NTE
                        'NAM': ['NAM', 'NWG'],  # Namuwongo Blazers / NWG
                        'JOH': ['JOH', 'JCA'],  # Johannesburg Giants (might be JCA)
                        'FBE': ['FBE', 'CFG'],  # Ferroviario Da Beira
                        'MMA': ['MMA', 'MOA'],  # Matero Magic (might be MOA)
                        'DAR': ['DAR', 'DCT'],  # Dar City
                        'BHB': ['BHB', 'BRA']   # Bravehearts
                    }
                    
                    # Find case study teams with variations
                    case_study_df_records = []
                    
                    for our_code, variations in case_study_codes_variations.items():
                        for var_code in variations:
                            matching = df[df['Team_Code'] == var_code]
                            if not matching.empty:
                                row = matching.iloc[0].copy()
                                row['Our_Code'] = our_code
                                case_study_df_records.append(row)
                                break
                    
                    if case_study_df_records:
                        case_study_df = pd.DataFrame(case_study_df_records)
                        
                        print("\n" + "=" * 80)
                        print("CASE STUDY TEAMS - ELITE 16 STANDINGS")
                        print("=" * 80)
                        print(case_study_df.to_string(index=False))
                        
                        # Save both files
                        df.to_csv('elite16_all_standings.csv', index=False)
                        print(f"\n✓ Saved all standings to elite16_all_standings.csv")
                        
                        case_study_df.to_csv('elite16_case_study_standings.csv', index=False)
                        print(f"✓ Saved case study standings to elite16_case_study_standings.csv")
                        
                        return case_study_df
                    else:
                        print("\n⚠ No case study teams found in standings")
                        # Save all standings anyway
                        df.to_csv('elite16_all_standings.csv', index=False)
                        print(f"✓ Saved all standings to elite16_all_standings.csv")
                        
                        # Show team codes to help identify
                        print("\nAvailable team codes:")
                        print(df[['Team_Code', 'Team_Name']].to_string(index=False))
                        
                        return df
                        
                except json.JSONDecodeError as e:
                    print(f"✗ JSON parsing error: {e}")
                    print("Trying alternative parsing method...")
            
            # Alternative: Parse games data directly
            print("\n\nParsing games data to extract team records...")
            
            # Find all team objects in the content
            teams_pattern = r'"teamId":(\d+).*?"code":"([A-Z]+)".*?"officialName":"([^"]+)".*?"teamAScore":(\d+),"teamBScore":(\d+)'
            
            # This is complex - let's try a simpler approach
            # Extract all occurrences of team codes and scores
            
        else:
            print("Games data structure not found")
            
    except Exception as e:
        print(f"✗ Error parsing JSON: {e}")
        import traceback
        traceback.print_exc()
    
    # Fallback: Try regex patterns to extract standings
    print("\n\nTrying regex-based extraction...")
    
    # Pattern for standings: "rank":1,"code":"ABC","wins":3,"losses":0
    standings_pattern = r'"rank":(\d+).*?"code":"([A-Z]+)".*?"officialName":"([^"]+)".*?"wins":(\d+).*?"losses":(\d+).*?"pointsFor":(\d+).*?"pointsAgainst":(\d+).*?"pointsDifference":(-?\d+).*?"points":(\d+)'
    
    matches = re.findall(standings_pattern, content)
    
    if matches:
        print(f"✓ Found {len(matches)} standings via regex")
        
        standings_list = []
        for match in matches:
            standings_list.append({
                'Rank': int(match[0]),
                'Team_Code': match[1],
                'Team_Name': match[2],
                'W': int(match[3]),
                'L': int(match[4]),
                'PF': int(match[5]),
                'PA': int(match[6]),
                'PD': int(match[7]),
                'PTS': int(match[8])
            })
        
        df_regex = pd.DataFrame(standings_list)
        print("\n" + "=" * 80)
        print("STANDINGS (REGEX EXTRACTION)")
        print("=" * 80)
        print(df_regex.to_string(index=False))
        
        df_regex.to_csv('elite16_standings_regex.csv', index=False)
        print(f"\n✓ Saved to elite16_standings_regex.csv")
        
        return df_regex
    else:
        print("✗ No standings found via regex")
    
    return None

if __name__ == "__main__":
    parse_elite16_data()
