import pandas as pd
import numpy as np
import random

class CarbonFootprintCalculator:
    def __init__(self):
        self.packaging_material_scores = {
            'plastic': 8,
            'cardboard': 4,
            'paper': 3,
            'glass': 5,
            'metal': 6,
            'biodegradable': 2
        }
        
        self.shipping_mode_scores = {
            'air': 10,
            'road': 6,
            'rail': 4,
            'sea': 5,
            'local': 2
        }
        
        # Brand adjustments based on sustainability practices (higher = worse for environment)
        # 1.0 is neutral, <1.0 is better, >1.0 is worse
        self.brand_adjustments = {
            'acana': 1.05, 'adguard': 0.95, 'aeg': 1.0, 'aehrolayf': 1.0, 'aerocool': 1.1, 
            'agu': 1.0, 'aiko': 1.0, 'aimoto': 1.0, 'airline': 1.15, 'aist': 1.0, 
            'akitio': 1.0, 'akku': 1.0, 'akpo': 1.0, 'aksion': 1.0, 'alex': 1.0, 
            'alfa': 1.0, 'alienware': 1.2, 'alinco': 1.0, 'alis': 1.0, 'alpengaudi': 1.0, 
            'alpina': 1.0, 'altel': 1.0, 'altex': 1.0, 'amazon': 1.15, 'amd': 1.1, 
            'anon': 1.0, 'anymode': 1.0, 'aoc': 1.05, 'aoki': 1.0, 'apacer': 1.0, 
            'apc': 1.05, 'apollo': 1.0, 'apple': 1.2, 'aqua': 1.0, 'aquael': 1.0, 
            'arena': 1.0, 'ariston': 1.05, 'arktika': 1.0, 'arnica': 1.0, 'art.fit': 1.0, 
            'art.home': 1.0, 'artberry': 1.0, 'asics': 1.0, 'asrock': 1.1, 'asus': 1.1, 
            'atlant': 1.0, 'atmor': 1.0, 'atom': 1.0, 'att': 1.0, 'audac': 1.0, 
            'author': 1.0, 'ava': 1.0, 'avel': 1.0, 'avermedia': 1.0, 'avrora': 1.0, 
            'awax': 1.0, 'awei': 1.0, 'axper': 1.0, 'babolat': 1.0, 'baboo': 1.0, 
            'babyliss': 1.0, 'barbie': 1.05, 'bardahl': 1.0, 'beats': 1.1, 'beeline': 1.0, 
            'beko': 1.0, 'belcando': 1.0, 'belita': 1.0, 'bellissima': 1.0, 'benq': 1.05, 
            'bequiet': 0.95, 'berghoff': 1.0, 'bestway': 1.05, 'beurer': 1.0, 'billna': 1.0, 
            'biol': 1.0, 'biolane': 0.9, 'biomio': 0.85, 'biostar': 1.0, 'birjusa': 1.0, 
            'bissell': 1.0, 'bjurokrat': 1.0, 'blackstar': 1.0, 'blackvue': 1.0, 'blehk': 1.0, 
            'bloody': 1.0, 'bork': 1.0, 'borner': 1.0, 'bosch': 0.95, 'bose': 1.1, 
            'bradex': 1.0, 'braun': 1.0, 'brother': 1.0, 'byintek': 1.0, 'bykski': 1.0, 
            'cablexpert': 1.0, 'camelion': 1.0, 'cannondale': 0.9, 'canon': 1.05, 'canyon': 1.0, 
            'cars': 1.1, 'casada': 1.0, 'casio': 1.0, 'caso': 1.0, 'cayin': 1.0, 
            'cdc': 1.0, 'celebrat': 1.0, 'chameleon': 1.0, 'char-broil': 1.1, 'chayka': 1.0, 
            'chicco': 1.0, 'china': 1.15, 'chistotel': 1.0, 'cilek': 1.0, 'cinemood': 1.0, 
            'citoderm': 1.0, 'cliny': 1.0, 'colorfix': 1.0, 'colorful': 1.0, 'compliment': 1.0, 
            'continent': 1.0, 'coolinar': 1.0, 'corsair': 1.1, 'cougar': 1.0, 'cremesso': 1.0, 
            'crucial': 1.0, 'cube': 1.0, 'cubicfun': 1.0, 'cullmann': 1.0, 'curver': 1.0, 
            'cyberpower': 1.1, 'cybex': 1.0, 'd-link': 1.0, 'dabur': 1.0, 'daewoo': 1.05, 
            'dahon': 0.9, 'daikin': 1.0, 'dauscher': 1.0, 'dc-girls': 1.0, 'decoroom': 1.0, 
            'deepcool': 1.0, 'defender': 1.0, 'dell': 0.9, 'delonghi': 1.0, 'delux': 1.0, 
            'deluxe': 1.0, 'demidovskiy': 1.0, 'depileve': 1.0, 'dewalt': 1.05, 'different': 1.0, 
            'dji': 1.05, 'dk': 1.0, 'dogland': 1.0, 'domini': 1.0, 'dougez': 1.0, 
            'duracell': 1.05, 'dxracer': 1.1, 'dynastar': 1.0, 'dyson': 1.05, 'e-blue': 1.0, 
            'eastcoast': 1.0, 'ecologystone': 0.8, 'edifier': 1.0, 'eglo': 1.0, 'ehra': 1.0, 
            'elari': 1.0, 'electrolux': 1.0, 'elfe': 1.0, 'elica': 1.0, 'energea': 1.0, 
            'epson': 1.05, 'er': 1.0, 'ergolux': 1.0, 'eset': 1.0, 'etalon': 1.0, 
            'eurolux': 1.0, 'europrint': 1.0, 'evere': 1.0, 'everlast': 1.0, 'eyfel': 1.0, 
            'ezetil': 1.0, 'ezviz': 1.0, 'feja': 1.0, 'fender': 1.0, 'fiio': 1.0, 
            'filtero': 1.0, 'filtrete': 1.0, 'finis': 1.0, 'fissman': 1.0, 'fly': 1.0, 
            'footwork': 1.0, 'fossil': 1.0, 'franke': 1.0, 'fsp': 1.0, 'fujifilm': 1.0, 
            'g.skill': 1.0, 'galaxy': 1.0, 'gamdias': 1.0, 'gamemax': 1.0, 'garanterm': 1.0, 
            'garmin': 1.0, 'gefest': 1.0, 'geil': 1.0, 'gembird': 1.0, 'gemon': 1.0, 
            'genau': 1.0, 'genius': 1.0, 'gerat': 1.0, 'gewa': 1.0, 'gezatone': 1.0, 
            'ggg': 1.0, 'giant': 0.9, 'gigabyte': 1.05, 'giottos': 1.0, 'glassware': 1.0, 
            'global': 1.0, 'globber': 1.0, 'goliath': 1.0, 'goodyear': 1.1, 'google': 1.0, 
            'gopro': 1.05, 'gorenje': 1.0, 'granchio': 1.0, 'grans': 1.0, 'greenway': 0.85, 
            'grillver': 1.0, 'grohe': 1.0, 'grundfos': 1.0, 'gtec': 1.0, 'gutrend': 1.0, 
            'hansa': 1.0, 'harper': 1.0, 'haushalt': 1.0, 'herschel': 1.0, 'highwaybaby': 1.0, 
            'hintek': 1.0, 'hitachi': 1.05, 'hms': 1.0, 'hoco': 1.0, 'honor': 1.05, 
            'hotpoint-ariston': 1.05, 'hoya': 1.0, 'hp': 1.0, 'huawei': 1.05, 'huion': 1.0, 
            'hukuba': 1.0, 'huntkey': 1.0, 'hurom': 1.0, 'huter': 1.0, 'hyperx': 1.05, 
            'hyundai': 1.05, 'id-cooling': 1.0, 'iiyama': 1.0, 'imbema': 1.0, 'imetec': 1.0, 
            'incase': 1.0, 'indesit': 1.0, 'inhouse': 1.0, 'inkax': 1.0, 'inoi': 1.0, 
            'insight': 1.0, 'inspector': 1.0, 'intel': 1.05, 'intex': 1.0, 'ipower': 1.0, 
            'irbis': 1.0, 'isolon': 1.0, 'ivi': 1.0, 'ivolia': 1.0, 'jabra': 1.0, 
            'jack': 1.0, 'jaguar': 1.05, 'jandeks': 1.0, 'janome': 1.0, 'jbl': 1.05, 
            'jetair': 1.1, 'jetpik': 1.0, 'joby': 1.0, 'joerex': 1.0, 'jonsbo': 1.0, 
            'joonies': 1.0, 'jose': 1.0, 'jvc': 1.0, 'kaabo': 1.0, 'karcher': 1.0, 
            'kaspersky': 1.0, 'kenko': 1.0, 'kenwood': 1.0, 'kerasys': 1.0, 'kicx': 1.0, 
            'kingston': 1.0, 'kink': 1.0, 'kitchenaid': 1.0, 'kiturami': 1.0, 'kivi': 1.0, 
            'kmk': 1.0, 'kodak': 1.05, 'kona': 1.0, 'korg': 1.0, 'kramet': 1.0, 
            'krups': 1.0, 'kumano': 1.0, 'kurzweil': 1.0, 'kyocera': 1.0, 'lamart': 1.0, 
            'lange': 1.0, 'laurastar': 1.0, 'lefard': 1.0, 'legrand': 1.0, 'lemark': 1.0, 
            'lenovo': 0.95, 'lg': 1.0, 'liebherr': 1.0, 'lihom': 1.0, 'lion': 1.0, 
            'loewe': 1.0, 'logitech': 1.0, 'lol': 1.0, 'lori': 1.0, 'lotte': 1.0, 
            'lowepro': 1.0, 'luch': 1.0, 'luxell': 1.0, 'maestro': 1.0, 'makita': 1.0, 
            'manfrotto': 1.0, 'mannol': 1.0, 'marcato': 1.0, 'marley': 1.0, 'marshall': 1.0, 
            'mart': 1.0, 'matrix': 1.0, 'mattel': 1.05, 'maxwell': 1.0, 'medela': 1.0, 
            'medisana': 1.0, 'megogo': 1.0, 'meizu': 1.0, 'melitta': 1.0, 'mercusys': 1.0, 
            'merries': 1.0, 'metabo': 1.0, 'micro': 1.0, 'microlab': 1.0, 'microsoft': 1.0, 
            'midea': 1.0, 'miele': 0.95, 'milan': 1.0, 'milight': 1.0, 'millet': 1.0, 
            'mio': 1.0, 'molnija': 1.0, 'momentum': 1.0, 'monge': 1.0, 'moshi': 1.0, 
            'motorola': 1.0, 'moulinex': 1.0, 'msep': 1.0, 'msi': 1.05, 'mujjo': 1.0, 
            'muljhtidom': 1.0, 'nakamichi': 1.0, 'navien': 1.0, 'navitel': 1.0, 'neo': 1.0, 
            'neoline': 1.0, 'neonode': 1.0, 'neptun': 1.0, 'netatmo': 1.0, 'nika': 1.0, 
            'nikon': 1.0, 'ninebot': 1.0, 'nintendo': 1.0, 'nissan': 1.1, 'noctua': 1.0, 
            'nokia': 1.0, 'nomi': 1.0, 'nommi': 1.0, 'none': 1.0, 'novatrack': 1.0, 
            'nuk': 1.0, 'nv-print': 1.0, 'nvidia': 1.1, 'nzxt': 1.05, 'okko': 1.0, 
            'olympus': 1.0, 'oma': 1.0, 'omron': 1.0, 'onanoff': 1.0, 'oppo': 1.05, 
            'optoma': 1.0, 'oral-b': 1.0, 'organ': 1.0, 'orico': 1.0, 'orion': 1.0, 
            'ozone': 1.0, 'paclan': 1.0, 'palisad': 1.0, 'palit': 1.0, 'panasonic': 1.0, 
            'pandora': 1.0, 'paperline': 1.0, 'parkcity': 1.0, 'patriot': 1.0, 'pccooler': 1.0, 
            'pedigree': 1.0, 'pemco': 1.0, 'perilla': 1.0, 'peterhof': 1.0, 'pgytech': 1.0, 
            'phantom': 1.0, 'philips': 1.0, 'pioneer': 1.0, 'plantronics': 1.0, 'playme': 1.0, 
            'plextor': 1.0, 'pocketbook': 1.0, 'polaris': 1.0, 'polaroid': 1.0, 'polimerbiht': 1.0, 
            'portcase': 1.0, 'powerplant': 1.0, 'pozis': 1.0, 'president': 1.0, 'prestigio': 1.0, 
            'procab': 1.0, 'proscreen': 1.0, 'provence': 1.0, 'puff': 1.0, 'pyrex': 1.0, 
            'qmax': 1.0, 'qnap': 1.0, 'raduga': 1.0, 'rapoo': 1.0, 'rastar': 1.0, 
            'razer': 1.1, 'redmond': 1.0, 'regnum': 1.0, 'remington': 1.0, 'reno': 1.0, 
            'resanta': 1.0, 'resto': 1.0, 'ride': 1.0, 'rinnai': 1.0, 'ritmix': 1.0, 
            'riva': 1.0, 'rivacase': 1.0, 'roca': 1.0, 'rocketbook': 1.0, 'roevuta': 1.0, 
            'roeyuta': 1.0, 'rondell': 1.0, 'rossija': 1.0, 'rowenta': 1.0, 'ruggear': 1.0, 
            'runwin': 1.0, 'sakura': 1.0, 'samsonite': 1.0, 'samsung': 1.1, 'sanc': 1.0, 
            'sandisk': 1.0, 'saramonic': 1.0, 'satechi': 1.0, 'savic': 1.0, 'sbs': 1.0, 
            'scarlett': 1.0, 'seagate': 1.0, 'seasonic': 1.0, 'sencor': 1.0, 'sennheiser': 1.0, 
            'shenzhen': 1.0, 'ship': 1.0, 'sibrtekh': 1.0, 'sigma': 1.0, 'simax': 1.0, 
            'simba': 1.0, 'simfer': 1.0, 'singer': 1.0, 'sjcam': 1.0, 'skullcandy': 1.0, 
            'skyworth': 1.0, 'smart': 1.0, 'smeg': 1.0, 'sonnet': 1.0, 'sony': 1.05, 
            'sonyamaguchi': 1.0, 'yiling': 1.0, 'yoobao': 1.0, 'zala': 1.0, 'zalman': 1.0, 
            'zenit': 1.0, 'zeppelin': 1.0, 'zeta': 1.0, 'zevs': 1.0, 'zhorka': 1.0, 
            'zlatek': 1.0, 'zowie': 1.0, 'zwilling': 1.0
        }
        
        self.category_weights = {
            'electronics.laptop': 1.2,
            'electronics.smartphone': 1.0,
            'electronics.tablet': 1.1,
            'electronics.headphone': 0.8,
            'home.appliance': 1.5
        }
    
    def calculate_usage_duration_score(self, duration_str):
        try:
            years = int(duration_str.split()[0])
            return max(1, 10 - years)
        except:
            return 5  
    
    def calculate_cf_score(self, row):
        # Get base scores
        packaging_score = self.packaging_material_scores.get(row['packaging_material'].lower(), 5)
        shipping_score = self.shipping_mode_scores.get(row['shipping_mode'].lower(), 5)
        usage_duration_score = self.calculate_usage_duration_score(row['usage_duration'])
        repairability_score = 10 - int(row['repairability_score'])  
        
        brand_adjustment = self.brand_adjustments.get(row['brand'], 1.0)
        
        category_weight = self.category_weights.get(row['category_code'], 1.0)
        
        base_cf_score = (
            (packaging_score * 2.5) +
            (shipping_score * 3.0) +
            (usage_duration_score * 2.5) +
            (repairability_score * 2.0)
        ) * brand_adjustment * category_weight
        
        normalized_score = min(100, max(0, base_cf_score))
        
        return normalized_score
    
    def classify_cf_score(self, score):
        if score >= 70:
            return "High CF"
        elif score >= 40:
            return "Medium CF"
        else:
            return "Low CF"
    
    def process_dataset(self, csv_path):
        """Process dataset and add CF scores"""
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Check if it's the large df_2.csv or the small data.csv
        if 'packaging_material' not in df.columns:
            # For df_2.csv, we need to add the sustainability columns
            print(f"Processing large dataset: {csv_path}")
            
            # Add random values for the sustainability columns
            # Define possible values for each column
            packaging_materials = ['plastic', 'cardboard', 'paper', 'glass', 'metal', 'biodegradable']
            shipping_modes = ['air', 'road', 'rail', 'sea', 'local']
            usage_durations = ['1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years']
            
            # Sample size - limit to 1000 rows for processing speed
            sample_size = min(1000, len(df))
            df_sample = df.sample(sample_size)
            
            # Add the sustainability columns with random values
            df_sample['packaging_material'] = [random.choice(packaging_materials) for _ in range(sample_size)]
            df_sample['shipping_mode'] = [random.choice(shipping_modes) for _ in range(sample_size)]
            df_sample['usage_duration'] = [random.choice(usage_durations) for _ in range(sample_size)]
            df_sample['repairability_score'] = [random.randint(1, 10) for _ in range(sample_size)]
            
            # Make sure brand column is lowercase for consistent matching
            df_sample['brand'] = df_sample['brand'].str.lower()
            
            # Calculate CF score for each product
            df_sample['cf_score'] = df_sample.apply(self.calculate_cf_score, axis=1)
            
            # Classify CF scores
            df_sample['cf_category'] = df_sample['cf_score'].apply(self.classify_cf_score)
            
            return df_sample
        else:
            # For data.csv, we already have all the required columns
            print(f"Processing small dataset: {csv_path}")
            
            # Calculate CF score for each product
            df['cf_score'] = df.apply(self.calculate_cf_score, axis=1)
            
            # Classify CF scores
            df['cf_category'] = df['cf_score'].apply(self.classify_cf_score)
            
            return df

if __name__ == "__main__":
    calculator = CarbonFootprintCalculator()
    
    # Process the small dataset by default
    result_df = calculator.process_dataset('data.csv')
    
    # To process the large dataset, uncomment the line below
    # result_df = calculator.process_dataset('df_2.csv')
    
    result_df.to_csv('data_with_cf_scores.csv', index=False)
    
    print(f"Average CF Score: {result_df['cf_score'].mean():.2f}")
    print(result_df['cf_category'].value_counts()) 