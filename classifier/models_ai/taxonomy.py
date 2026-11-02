"""
Taxonomy and Domain Knowledge Base for Multi-Category Image Classification.
Covers 5 core domains: Plants, Animals, Vehicles, Waste Materials, and Medical Imaging.
"""

DOMAINS = {
    'plants': {
        'id': 'plants',
        'name': 'Plant & Leaf Analysis',
        'badge': 'Agriculture AI',
        'icon': '🌱',
        'color': '#10b981',
        'accent_gradient': 'linear-gradient(135deg, #059669, #10b981)',
        'description': 'Identifies plant species and distinguishes healthy leaves from diseased specimens (blights, rusts, scabs) to assist preliminary agricultural screening.',
        'classes': [
            'Tomato Early Blight',
            'Potato Late Blight',
            'Apple Scab Disease',
            'Corn Common Rust',
            'Healthy Green Crop / Leaf',
            'Strawberry Leaf Scorch'
        ]
    },
    'animals': {
        'id': 'animals',
        'name': 'Animal & Wildlife Recognition',
        'badge': 'Fauna & Biodiversity',
        'icon': '🦁',
        'color': '#3b82f6',
        'accent_gradient': 'linear-gradient(135deg, #2563eb, #38bdf8)',
        'description': 'Recognizes diverse animal species and taxonomic groups based on morphological features, fur/feather patterns, and structural characteristics.',
        'classes': [
            'Dog (Canine Companion)',
            'Cat (Feline Domestic)',
            'Bird / Raptor (Avian Species)',
            'Horse (Equine Mammal)',
            'Lion (Panthera Leo)',
            'Elephant (African / Asian Proboscidean)',
            'Butterfly (Lepidoptera Pollinator)',
            'Giant Panda (Ailuropoda Melanoleuca)'
        ]
    },
    'vehicles': {
        'id': 'vehicles',
        'name': 'Vehicle & Transportation Classification',
        'badge': 'Smart Mobility',
        'icon': '🚗',
        'color': '#8b5cf6',
        'accent_gradient': 'linear-gradient(135deg, #7c3aed, #a855f7)',
        'description': 'Classifies vehicle modes including sedans, commercial buses, trucks, motorcycles, aircraft, and watercraft for intelligent transportation systems.',
        'classes': [
            'Passenger Sedan / Car',
            'Commercial Transit Bus',
            'Motorcycle / Motorbike',
            'Heavy Freight Cargo Truck',
            'Commuter Bicycle',
            'Commercial Aircraft / Airplane',
            'Maritime Cargo / Speed Boat'
        ]
    },
    'waste': {
        'id': 'waste',
        'name': 'Waste & Recyclable Segregation',
        'badge': 'Sustainability AI',
        'icon': '♻️',
        'color': '#f59e0b',
        'accent_gradient': 'linear-gradient(135deg, #d97706, #fbbf24)',
        'description': 'Distinguishes recyclable polymers, paper/cardboard, glass, and metals from organic compostables and hazardous electronic e-waste.',
        'classes': [
            'Plastic Bottle & Polymers (Recyclable)',
            'Paper & Cardboard Fiber (Recyclable)',
            'Glass Container & Jars (Recyclable)',
            'Metal / Aluminum Can (Recyclable)',
            'Organic & Biodegradable Food Waste',
            'Electronic E-Waste & Circuitry (Hazardous)'
        ]
    },
    'medical': {
        'id': 'medical',
        'name': 'Medical Imaging & Clinical Screening',
        'badge': 'Healthcare Research',
        'icon': '🩻',
        'color': '#ef4444',
        'accent_gradient': 'linear-gradient(135deg, #dc2626, #f87171)',
        'description': 'Demonstrates deep learning visual pattern detection on thoracic X-rays, neuroimaging, and dermatological lesion scans for educational/research purposes.',
        'disclaimer': 'EDUCATIONAL/RESEARCH DEMONSTRATION ONLY: This AI model is not a medical device and must never be used as a substitute for professional clinical diagnosis, physician evaluation, or healthcare decisions.',
        'classes': [
            'Normal Thoracic Chest X-Ray',
            'Pneumonia Pulmonary Consolidation X-Ray',
            'Cardiomegaly Cardiac Silhouette X-Ray',
            'Brain MRI Scan (Cerebral Imaging)',
            'Benign Melanocytic Nevus / Mole',
            'High-Risk Suspicious Skin Lesion (Screening Referral)'
        ]
    }
}

CLASS_DETAILS = {
    # Plants
    'Tomato Early Blight': {
        'domain': 'plants',
        'status': 'Pathogenic Foliar Disease',
        'pathogen': 'Alternaria solani',
        'symptoms': 'Concentric brown-black circular rings ("target board" pattern) with yellow chlorotic halos on lower leaves.',
        'recommendation': 'Remove infected lower foliage immediately. Improve airflow, avoid overhead watering, and apply approved copper-based or bio-fungicide treatment.',
        'severity': 'Moderate - High',
        'eco_note': 'Early intervention prevents spread to entire crop.'
    },
    'Potato Late Blight': {
        'domain': 'plants',
        'status': 'High Risk Oomycete Infection',
        'pathogen': 'Phytophthora infestans',
        'symptoms': 'Water-soaked irregular dark lesions on leaf tips and margins; white fuzzy fungal growth under humid conditions.',
        'recommendation': 'Isolate affected plants. Destroy severely infected haulms. Maintain soil drainage and apply targeted defensive agricultural protection.',
        'severity': 'Critical',
        'eco_note': 'Historically notorious for potato crop devastations; requires prompt containment.'
    },
    'Apple Scab Disease': {
        'domain': 'plants',
        'status': 'Fungal Foliar & Fruit Infection',
        'pathogen': 'Venturia inaequalis',
        'symptoms': 'Dull olive-green to velvety brown lesions on leaves and fruit surfaces, causing leaf distortion and premature defoliation.',
        'recommendation': 'Rake and destroy fallen leaves in autumn to eliminate overwintering spores. Prune canopy for sunlight penetration; apply preventative horticultural spray.',
        'severity': 'Moderate',
        'eco_note': 'Can reduce orchard yield significantly if untreated in spring.'
    },
    'Corn Common Rust': {
        'domain': 'plants',
        'status': 'Fungal Rust Infection',
        'pathogen': 'Puccinia sorghi',
        'symptoms': 'Elongated powdery reddish-brown pustules (uredinia) scattered across upper and lower leaf surfaces.',
        'recommendation': 'Plant resistant maize hybrids. Monitor field humidity and threshold levels before applying foliar fungicides.',
        'severity': 'Moderate',
        'eco_note': 'Prevalent in cool, moist weather; spores spread easily on air currents.'
    },
    'Healthy Green Crop / Leaf': {
        'domain': 'plants',
        'status': 'Optimal Plant Vigour',
        'pathogen': 'None (Healthy)',
        'symptoms': 'Vibrant uniform chlorophyll pigmentation, intact epidermal margins, active photosynthetic surface.',
        'recommendation': 'Maintain balanced N-P-K nutrient supply, regular moisture schedule, and continue routine crop scouting.',
        'severity': 'Optimal',
        'eco_note': 'Strong healthy foliage reflects optimal soil health and effective pest management.'
    },
    'Strawberry Leaf Scorch': {
        'domain': 'plants',
        'status': 'Foliar Fungal Infection',
        'pathogen': 'Diplocarpon earlianum',
        'symptoms': 'Numerous small purple-brown blotches that coalesce, giving entire leaf an autumnal scorched or burned appearance.',
        'recommendation': 'Ensure wide row spacing for canopy aeration. Remove scorched leaves after harvest and implement drip irrigation.',
        'severity': 'Low - Moderate',
        'eco_note': 'Sanitation during post-harvest renovation suppresses pathogen carryover.'
    },

    # Animals
    'Dog (Canine Companion)': {
        'domain': 'animals',
        'status': 'Canis lupus familiaris',
        'symptoms': 'Quadrupedal mammal, erect or floppy ears, muzzle structure, tail wagging, distinctive canine facial anatomy.',
        'recommendation': 'Companion domestic animal. Requires balanced canine nutrition, regular vaccinations, mental enrichment, and daily physical exercise.',
        'severity': 'Domestic Fauna',
        'eco_note': 'First domesticated species, showing immense breed morphological diversity.'
    },
    'Cat (Feline Domestic)': {
        'domain': 'animals',
        'status': 'Felis catus',
        'symptoms': 'Compact carnivore anatomy, slit-pupil ocular structure, retractable claws, whiskers, agile muscular build.',
        'recommendation': 'Domestic pet. Provide species-appropriate protein diet, scratching surfaces, and indoor enrichment for feline wellbeing.',
        'severity': 'Domestic Fauna',
        'eco_note': 'Effective natural pest controller; keep indoors to safeguard local songbird biodiversity.'
    },
    'Bird / Raptor (Avian Species)': {
        'domain': 'animals',
        'status': 'Aves Class',
        'symptoms': 'Feathered plumage, keratinous beak, hollow skeletal adaptations, aerodynamic wings, keen binocular eyesight.',
        'recommendation': 'Wild avian specimen. Observe from respectful distance without disturbing nesting sites or habitats.',
        'severity': 'Wild / Migratory Fauna',
        'eco_note': 'Key bio-indicators for ecosystem health, insect regulation, and seed dispersal.'
    },
    'Horse (Equine Mammal)': {
        'domain': 'animals',
        'status': 'Equus caballus',
        'symptoms': 'Large ungulate, single-toed hooves, elongated head, flowing mane and tail, robust muscular physique.',
        'recommendation': 'Requires dedicated equine pasture, forage-based fiber diet, regular hoof trimming, and clean water access.',
        'severity': 'Domestic / Equine',
        'eco_note': 'Historically foundational to transport, agriculture, and equine athletic companionship.'
    },
    'Lion (Panthera Leo)': {
        'domain': 'animals',
        'status': 'Apex Predator Mammal',
        'symptoms': 'Large felid, sexual dimorphism (male mane), tawny coat, muscular shoulder structure, pride social behavior.',
        'recommendation': 'Vulnerable apex predator. Protect native savannah habitats and support wildlife anti-poaching reserves.',
        'severity': 'Vulnerable Wild Fauna',
        'eco_note': 'Crucial keystone predator regulating herbivore populations across African ecosystems.'
    },
    'Elephant (African / Asian Proboscidean)': {
        'domain': 'animals',
        'status': 'Keystone Megafauna',
        'symptoms': 'Elongated prehensile trunk, ivory incisor tusks, broad fan-shaped ears, column-like pillar legs.',
        'recommendation': 'Endangered megaherbivore. Strict global enforcement of anti-poaching laws and preservation of migration corridors.',
        'severity': 'Endangered Wild Fauna',
        'eco_note': 'Ecosystem engineers: they create waterholes, disperse giant seeds, and shape savannah landscapes.'
    },
    'Butterfly (Lepidoptera Pollinator)': {
        'domain': 'animals',
        'status': 'Insecta Lepidoptera',
        'symptoms': 'Four membranous wings coated in microscopic microscopic scales, clubbed antennae, coiled proboscis.',
        'recommendation': 'Plant native nectar and host flora (such as milkweed, salvia) and eliminate chemical pesticide runoff in gardens.',
        'severity': 'Beneficial Pollinator',
        'eco_note': 'Vital pollinators undergoing global population pressure; essential for plant reproduction.'
    },
    'Giant Panda (Ailuropoda Melanoleuca)': {
        'domain': 'animals',
        'status': 'Endangered / Vulnerable Bear',
        'symptoms': 'Distinctive black-and-white pelage, black eye patches, round bear head, specialized pseudo-thumb for gripping bamboo.',
        'recommendation': 'Protect high-altitude bamboo forest corridors and support international conservation breeding programs.',
        'severity': 'Conservation Success Species',
        'eco_note': 'Conservation flagship species symbolizing international biodiversity protection efforts.'
    },

    # Vehicles
    'Passenger Sedan / Car': {
        'domain': 'vehicles',
        'status': 'Personal Passenger Transport',
        'symptoms': 'Three-box configuration (engine, cabin, boot), four road wheels, aerodynamic low ground clearance silhouette.',
        'recommendation': 'Follow scheduled vehicle maintenance, maintain proper tyre PSI, and adopt eco-driving habits to reduce emissions.',
        'severity': 'Highway / City Mobility',
        'eco_note': 'Transition toward electric propulsion (EV) significantly cuts lifecycle carbon footprint.'
    },
    'Commercial Transit Bus': {
        'domain': 'vehicles',
        'status': 'Mass Public Transit',
        'symptoms': 'High-capacity elongated passenger body, multiple doors, elevated windshield, boxy transit chassis.',
        'recommendation': 'Prioritize dedicated bus rapid transit (BRT) lanes and transition fleets to zero-emission hydrogen/battery electric.',
        'severity': 'Public Transit Infrastructure',
        'eco_note': 'One full bus replaces up to 40 personal motor cars, drastically easing urban congestion.'
    },
    'Motorcycle / Motorbike': {
        'domain': 'vehicles',
        'status': 'Two-Wheeled Motorized Transport',
        'symptoms': 'Inline two wheels, handle-bar steering, exposed powertrain, rider saddle seating configuration.',
        'recommendation': 'Always wear DOT/ECE certified helmets, high-visibility protective gear, and practice defensive riding.',
        'severity': 'Compact Mobility',
        'eco_note': 'Lower fuel consumption and road space requirement compared to standard cars.'
    },
    'Heavy Freight Cargo Truck': {
        'domain': 'vehicles',
        'status': 'Heavy Commercial Logistics',
        'symptoms': 'Multi-axle chassis, heavy-duty cab-over or long-nose tractor unit, large trailer container.',
        'recommendation': 'Mandate electronic logbooks for driver rest, implement aerodynamic side skirts, and inspect brake systems regularly.',
        'severity': 'Interstate Logistics',
        'eco_note': 'Logistics backbone carrying goods; aerodynamic optimization saves thousands of gallons of fuel.'
    },
    'Commuter Bicycle': {
        'domain': 'vehicles',
        'status': 'Non-Motorized Active Mobility',
        'symptoms': 'Tubular diamond or step-through frame, two spoked wheels, pedal drivetrain, lightweight handlebars.',
        'recommendation': 'Utilize protected bike paths, fit front/rear safety lights, and wear approved cycling helmets.',
        'severity': 'Zero Emission Active Transport',
        'eco_note': 'True zero-emission transport offering tremendous public health and cardiovascular benefits.'
    },
    'Commercial Aircraft / Airplane': {
        'domain': 'vehicles',
        'status': 'Aviation Transport',
        'symptoms': 'Fixed-wing aerodynamic design, jet turbofans or turboprops, pressurized cylindrical fuselage, empennage tail.',
        'recommendation': 'Adhere to rigorous FAA/EASA airworthiness directives and advance Sustainable Aviation Fuel (SAF) adoption.',
        'severity': 'Airspace Logistics',
        'eco_note': 'Long-distance high-speed mobility; focus of intense research into green hydrogen and SAF fuels.'
    },
    'Maritime Cargo / Speed Boat': {
        'domain': 'vehicles',
        'status': 'Waterborne Navigation Vessel',
        'symptoms': 'V-hull or displacement hull, marine propulsion, navigation deck, watercraft water displacement profile.',
        'recommendation': 'Ensure life jackets for all passengers, inspect bilge pumps, maintain marine radio and GPS beacons.',
        'severity': 'Maritime Transport',
        'eco_note': 'Maritime freight handles over 80% of global trade by volume; adopting wind-assist rotors cuts fuel burn.'
    },

    # Waste
    'Plastic Bottle & Polymers (Recyclable)': {
        'domain': 'waste',
        'status': 'Recyclable Polymer (PET #1 / HDPE #2)',
        'symptoms': 'Molded polymer resin, transparent or tinted bottle form, synthetic neck and thread cap.',
        'recommendation': 'Empty liquids completely, rinse, crush to reduce volume, replace cap, and place into BLUE recycling bin.',
        'severity': 'Recyclable Stream',
        'eco_note': 'PET bottles can be recycled into polyester fleece, new beverage bottles, and durable industrial fiber.'
    },
    'Paper & Cardboard Fiber (Recyclable)': {
        'domain': 'waste',
        'status': 'Recyclable Cellulose Fiber',
        'symptoms': 'Corrugated flute layers or sheet paper, matte fibrous texture, wood pulp material.',
        'recommendation': 'Keep completely clean and dry! Flatten cardboard boxes. Avoid greasy pizza box liners (compost greasy portions). Place in BLUE/GREEN recycling bin.',
        'severity': 'Recyclable Stream',
        'eco_note': 'Cardboard can be recycled 5-7 times before fibers become too short to bind.'
    },
    'Glass Container & Jars (Recyclable)': {
        'domain': 'waste',
        'status': '100% Infinitely Recyclable Vitreous Material',
        'symptoms': 'Rigid amorphous solid, crystalline transparency, hard smooth non-porous surface.',
        'recommendation': 'Rinse thoroughly to remove food residue. Separate metal or plastic lids if required locally. Place in designated GLASS recycling receptacle.',
        'severity': 'Infinite Recyclable',
        'eco_note': 'Glass does not lose quality through recycling; recycled cullet melts at lower energy temperatures.'
    },
    'Metal / Aluminum Can (Recyclable)': {
        'domain': 'waste',
        'status': 'Valuable Non-Ferrous & Ferrous Metal',
        'symptoms': 'Drawn aluminum cylinder or tinplate steel can, metallic sheen, lightweight rigid seam.',
        'recommendation': 'Rinse beverage or food can. Do not crush if local optical sorting systems prefer 3D shapes. Deposit in METAL recycling stream.',
        'severity': 'High-Value Recyclable',
        'eco_note': 'Recycling aluminum consumes 95% less energy than extracting raw aluminum from bauxite ore.'
    },
    'Organic & Biodegradable Food Waste': {
        'domain': 'waste',
        'status': 'Compostable Organic Matter',
        'symptoms': 'Fruit peels, vegetable scraps, coffee grounds, discarded organic matter without synthetic coatings.',
        'recommendation': 'Divert to brown organics bin or home compost pile. Mix with dry leaves (brown carbon) for rich garden humus.',
        'severity': 'Compost Stream',
        'eco_note': 'Diverting organic waste from landfills prevents anaerobic decomposition and harmful methane emissions.'
    },
    'Electronic E-Waste & Circuitry (Hazardous)': {
        'domain': 'waste',
        'status': 'Hazardous / Valuable WEEE Stream',
        'symptoms': 'Printed circuit boards (PCBs), electronic solder, wiring, battery components, semiconductors.',
        'recommendation': 'NEVER throw into general trash or standard recycling! Take to certified e-waste municipal drop-off depot.',
        'severity': 'Hazardous Waste - Special Handling',
        'eco_note': 'Contains hazardous lead/cadmium alongside precious gold/copper; requires specialized urban mining.'
    },

    # Medical
    'Normal Thoracic Chest X-Ray': {
        'domain': 'medical',
        'status': 'Normal Pulmonary Radiograph',
        'symptoms': 'Clear lung fields without consolidation, sharp costophrenic angles, normal cardiothoracic ratio (< 0.50), intact ribs.',
        'recommendation': 'No acute pulmonary abnormality detected on visual screening. Correlate with clinical history and vital signs.',
        'severity': 'Baseline Normal',
        'eco_note': 'Important baseline comparator in radiological AI training and clinical evaluation.'
    },
    'Pneumonia Pulmonary Consolidation X-Ray': {
        'domain': 'medical',
        'status': 'Suspicious Pulmonary Opacity / Infiltrate',
        'symptoms': 'Patchy or dense focal alveolar opacification, air bronchograms, blurred hemidiaphragm or cardiac border.',
        'recommendation': 'CLINICAL ALERT: Findings suggestive of pulmonary consolidation. Immediate correlation with clinical stethoscope exam, sputum culture, and radiologist review advised.',
        'severity': 'Moderate - Urgent Clinical Followup',
        'eco_note': 'Automated CNN screening aids triage prioritizing critical thoracic scans in busy emergency departments.'
    },
    'Cardiomegaly Cardiac Silhouette X-Ray': {
        'domain': 'medical',
        'status': 'Cardiothoracic Enlargement (> 50%)',
        'symptoms': 'Widened cardiac silhouette occupying greater than 50% of maximal thoracic transverse diameter on PA projection.',
        'recommendation': 'CLINICAL ALERT: Suggests ventricular hypertrophy, pericardial effusion, or cardiomyopathy. Recommend prompt echocardiogram and cardiology consultation.',
        'severity': 'High Clinical Significance',
        'eco_note': 'Chest radiography remains the primary first-line screening modality worldwide.'
    },
    'Brain MRI Scan (Cerebral Imaging)': {
        'domain': 'medical',
        'status': 'Neuroimaging Section (T1/T2/FLAIR)',
        'symptoms': 'Detailed cerebral cortex, ventricular symmetry, gray-white matter differentiation, brainstem architecture.',
        'recommendation': 'Check for midline shift, hyperintense focal lesions, or ventricular dilatation. Requires board-certified neuroradiologist reading.',
        'severity': 'Diagnostic Neuroimaging',
        'eco_note': 'High-resolution multi-planar magnetic resonance imaging without ionizing radiation.'
    },
    'Benign Melanocytic Nevus / Mole': {
        'domain': 'medical',
        'status': 'Benign Dermatological Lesion',
        'symptoms': 'Symmetrical circular borders, uniform brown/tan pigmentation, diameter under 6mm, stable unchanging evolution.',
        'recommendation': 'Follow the ABCDE melanoma rule. Perform monthly self-skin checks; consult a dermatologist if change in color, border, or size occurs.',
        'severity': 'Low Risk / Benign',
        'eco_note': 'Routine skin cancer screenings catch dangerous melanoma at the most curable early stages.'
    },
    'High-Risk Suspicious Skin Lesion (Screening Referral)': {
        'domain': 'medical',
        'status': 'Atypical Dermatological Lesion - Referral Indicated',
        'symptoms': 'Asymmetrical architecture, notched or scalloped irregular borders, variegated multi-tone coloring, diameter > 6mm.',
        'recommendation': 'URGENT DERMATOLOGY EVALUATION: Suspicious visual features detected. Immediate in-person dermatoscopy and potential biopsy recommended.',
        'severity': 'High Risk Screening Flag',
        'eco_note': 'Early detection of melanoma drastically improves 5-year survival rates above 99%.'
    }
}
