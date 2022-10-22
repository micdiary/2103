LOCK TABLES `polytechnic` WRITE;
INSERT INTO `polytechnic` VALUES (1,'R','RP',3086.50,6316.50,11541.10),(2,'T','TP',2041.60,6241.60,11464.10),(3,'S','SP',3076.79,6306.79,11531.39),(4,'N','NP',3000.00,6200.00,11400.00),(5,'C','NYP',3087.00,6317.00,11541.60);
UNLOCK TABLES;

LOCK TABLES `school` WRITE;
INSERT INTO `school` VALUES (1,'School of Applied Science',1),(2,'School of Engineering',1),(3,'School of Hospitality',1),(4,'School of Infocomm',1),(5,'School of Sports Health and Leisure',1),(6,'School of Management and Communication',1),(7,'School of Technology for the Arts',1),(8,'School of Applied Science',2),(9,'School of Business',2),(10,'School of Engineering',2),(11,'School of Humanities & Social Sciences',2),(12,'School of Informatics & IT',2),(13,'School of Design',2),(14,'Applied Sciences',3),(15,'Bulit Environment',3),(16,'Business Management',3),(17,'Engineering',3),(18,'Health Sciences',3),(19,'Information & Digital Technologies',3),(20,'Maritime Studies',3),(21,'Media & Design',3),(22,'School of Business & Accountancy',4),(23,'School of Design & Environment',4),(24,'School of Engineering',4),(25,'School of Film & Media Studies',4),(26,'School of Health Sciences',4),(27,'School of Humanities & Social Sciences',4),(28,'School of InfoComm Technology',4),(29,'School of Life Sciences & Chemical Technology',4),(30,'School Of Applied Science',5),(31,'School Of Business Management',5),(32,'School Of Design & Media',5),(33,'School Of Engineering',5),(34,'School Of Health & Social Sciences',5),(35,'School Of Information Technology',5);
UNLOCK TABLES;

LOCK TABLES `course` WRITE;
INSERT INTO `course` VALUES (1786,'Applied Chemistry',100,14,'S64',5,9),(1787,'Biomedical Science',100,14,'S98',3,7),(1788,'Chemical Engineering',120,14,'S70',5,13),(1789,'Common Science Programme',0,14,'S28',0,0),(1790,'Food Science & Technology',105,14,'S47',5,13),(1791,'Perfumery & Cosmetic Science',50,14,'S38',5,11),(1792,'Architecture',95,15,'S66',5,13),(1793,'Civil Engineering',120,15,'S68',7,20),(1794,'Facilities Management',75,15,'S95',11,19),(1795,'Integrated Events & Project Management',100,15,'S50',5,16),(1796,'Landscape Architecture',40,15,'S94',8,15),(1797,'Accountancy',100,16,'S75',3,12),(1798,'Banking & Finance',80,16,'S76',6,12),(1799,'Business Administration',120,16,'S71',4,12),(1800,'Common Business Programme',205,16,'S31',4,12),(1801,'Human Resource Management with Psychology',100,16,'S48',5,12),(1802,'Aeronautical Engineering',180,17,'S88',5,17),(1803,'Aerospace Electronics',90,17,'S90',7,13),(1804,'Common Engineering Programme',340,17,'S40',7,17),(1805,'Computer Engineering',215,17,'S53',3,12),(1806,'Electrical & Electronic Engineering',220,17,'S99',6,17),(1807,'Engineering with Business',60,17,'S42',5,11),(1808,'Mechanical Engineering',180,17,'S91',4,17),(1809,'Mechatronics & Robotics',75,17,'S73',5,13),(1810,'Optometry',60,18,'S67',6,12),(1811,'Applied AI & Analytics',80,19,'S30',3,8),(1812,'Common ICT Programme',165,19,'S32',3,13),(1813,'Infocomm Security Management',120,19,'S54',4,11),(1814,'Information Technology',160,19,'S69',4,14),(1815,'Marine Engineering',115,20,'S63',7,22),(1816,'Maritime Business',120,20,'S74',7,18),(1817,'Nautical Studies',40,20,'DNS',0,0),(1818,'Interior Design',60,21,'S89',4,14),(1819,'Media Arts & Design',414,21,'S29',4,12),(1820,'Diploma in Accountancy',135,22,'N51',4,11),(1821,'Diploma in Banking & Finance',75,22,'N53',4,11),(1822,'Diploma in Business Studies',150,22,'N45',4,9),(1823,'Common Business Programme',220,22,'N97',4,12),(1824,'Diploma in International Trade & Business',75,22,'N85',6,12),(1825,'Diploma in Tourism & Resort Management',50,22,'N72',5,13),(1826,'Diploma in Design',75,23,'N12',6,14),(1827,'Diploma in Hotel & Leisure Facilities Management',95,23,'N40',11,17),(1828,'Diploma in Real Estate Business',70,23,'N48',9,15),(1829,'Diploma in Aerospace Engineering',100,24,'N65',3,16),(1830,'Diploma in Automation & Mechatronic Systems',55,24,'N50',7,20),(1831,'Diploma in Biomedical Engineering',60,24,'N60',4,12),(1832,'Common Engineering Programme',350,24,'N71',3,19),(1833,'Diploma in Electrical Engineering',95,24,'N43',11,20),(1834,'Diploma in Electronic & Computer Engineering',135,24,'N44',6,16),(1835,'Diploma in Engineering Science',50,24,'N93',4,12),(1836,'Diploma in Marine & Offshore Technology',40,24,'N42',13,18),(1837,'Diploma in Mechanical Engineering',120,24,'N41',12,22),(1838,'Diploma in Film Sound & Video',55,25,'N82',4,12),(1839,'Diploma in Mass Communication',110,25,'N67',4,10),(1840,'Diploma in Media Post-Production',55,25,'N13',6,13),(1841,'Diploma in Nursing',600,26,'N69',4,28),(1842,'Diploma in Optometry',45,26,'N83',9,13),(1843,'Diploma in Arts Business Management',40,27,'N91',5,9),(1844,'Diploma in Chinese Media & Communication',40,27,'N88',6,11),(1845,'Diploma in Chinese Studies',50,27,'N70',7,13),(1846,'Diploma in Community Development',85,27,'N11',4,10),(1847,'Diploma in Early Childhood Development & Education',500,27,'N96',5,18),(1848,'Diploma in Tamil Studies with Early Education',30,27,'N95',15,21),(1849,'Common ICT Programme',125,28,'N98',6,13),(1850,'Diploma in Cybersecurity & Digital Forensics',50,28,'N94',3,8),(1851,'Diploma in Data Science',50,28,'N81',6,11),(1852,'Diploma in Immersive Media',50,28,'N55',8,16),(1853,'Diploma in Information Technology',100,28,'N54',6,15),(1854,'Diploma in Biomedical Science',85,29,'N59',4,8),(1855,'Diploma in Chemical & Biomolecular Engineering',75,29,'N56',6,11),(1856,'Diploma in Environmental & Water Technology',45,29,'N74',5,14),(1857,'Diploma in Landscape Design & Horticulture',40,29,'N57',8,16),(1858,'Diploma in Pharmaceutical Science',50,29,'N73',5,9),(1859,'Chemical Engineering',150,8,'T33',6,15),(1860,'Food Nutrition & Culinary Science',70,8,'T26',8,14),(1861,'Medical Biotechnology',100,8,'T64',3,10),(1862,'Pharmaceutical Science',100,8,'T25',7,11),(1863,'Veterinary Technology',70,8,'T45',3,10),(1864,'Accountancy & Finance',115,9,'T02',4,13),(1865,'Business',170,9,'T10',5,14),(1866,'Common Business Programme',300,9,'T01',5,15),(1867,'Communications & Media Management',85,9,'T40',3,13),(1868,'Culinary & Catering Management',70,9,'T18',5,17),(1869,'Hospitality & Tourism Management',125,9,'T08',9,18),(1870,'Law & Management',110,9,'T09',6,11),(1871,'International Trade & Logistics',70,9,'T07',8,17),(1872,'Marketing',75,9,'T67',5,15),(1873,'Aerospace Electronics',75,10,'T50',8,18),(1874,'Aerospace Engineering',100,10,'T51',4,16),(1875,'Architectural Technology & Building Services',75,10,'T29',6,16),(1876,'Aviation Management',75,10,'T04',6,14),(1877,'Biomedical Engineering',100,10,'T38',6,13),(1878,'Business Process & Systems Engineering',100,10,'T43',8,18),(1879,'Common Engineering Programme',475,10,'T56',7,22),(1880,'Computer Engineering',100,10,'T13',5,13),(1881,'Electronics',50,10,'T65',9,16),(1882,'Integrated Facility Management',100,10,'T28',14,20),(1883,'Mechatronics',50,10,'T66',11,16),(1884,'Early Childhood Development & Education',260,11,'T68',5,20),(1885,'Psychology Studies',75,11,'T48',3,8),(1886,'Social Sciences in Gerontology',50,11,'T53',10,14),(1887,'Applied Artificial Intelligence',50,12,'T69',5,12),(1888,'Big Data & Analytics',50,12,'T60',6,12),(1889,'Common ICT Programme',195,12,'T63',4,16),(1890,'Cybersecurity & Digital Forensics',150,12,'T62',4,12),(1891,'Game Design & Development',50,12,'T58',9,14),(1892,'Information Technology',100,12,'T30',5,16),(1893,'Apparel Design & Merchandising',70,13,'T20',6,11),(1894,'Communication Design',95,13,'T59',6,15),(1895,'Digital Film & Television',75,13,'T23',5,14),(1896,'Interior Architecture & Design',75,13,'T22',8,14),(1897,'Product & Industrial Design',50,13,'T35',9,17),(1898,'Biomedical Science',97,1,'R14',8,11),(1899,'Biotechnology',85,1,'R16',10,17),(1900,'Applied Chemistry',47,1,'R17',11,17),(1901,'Pharmaceutical Science',148,1,'R22',9,17),(1902,'Common Science Programme',186,1,'R59',7,13),(1903,'Environmental & Marine Science',61,1,'R62',7,18),(1904,'Industrial & Operations Management',80,2,'R11',12,26),(1905,'Supply Chain Management',80,2,'R21',11,25),(1906,'Aviation Management',84,2,'R39',16,25),(1907,'Aerospace Engineering',95,2,'R40',17,26),(1908,'Common Engineering Programme',285,2,'R42',18,26),(1909,'Electrical & Electronic Engineering',123,2,'R50',16,24),(1910,'Engineering Systems & Management',62,2,'R54',16,24),(1911,'Engineering Design with Business',65,2,'R56',13,26),(1912,'Sustainable Built Environment',50,2,'R61',15,26),(1913,'Integrated Events Management',120,3,'R28',15,26),(1914,'Customer Experience Management with Business   ',112,3,'R34',12,21),(1915,'Hotel & Hospitality Management   ',100,3,'R37',14,26),(1916,'Restaurant & Culinary Operations',60,3,'R46',10,26),(1917,'Information Technology ',125,4,'R12',15,26),(1918,'Business Information Systems  ',118,4,'R13',15,26),(1919,'Financial Technology',115,4,'R18',15,26),(1920,'Digital Design & Development',75,4,'R47',13,24),(1921,'Infocomm Security Management',84,4,'R55',13,22),(1922,'Common ICT Programme ',215,4,'R58',16,26),(1923,'Sport & Exercise Science',97,5,'R26',6,16),(1924,'Outdoor & Adventure Learning ',45,5,'R33',18,26),(1925,'Health Management & Promotion ',75,5,'R43',13,26),(1926,'Health Services Management ',75,5,'R45',16,26),(1927,'Sport Coaching',44,5,'R49',10,18),(1928,'Common Sports and Health Programme',141,5,'R63',11,26),(1929,'Mass Communication',115,6,'R32',9,16),(1930,'Consumer Behaviour & Research',69,6,'R48',13,18),(1931,'Human Resource Management with Psychology ',70,6,'R52',11,16),(1932,'\"Common Business Programme	\"',276,6,'R57',13,26),(1933,'Business',125,6,'R60',15,21),(1934,'Media Production & Design   ',118,7,'R19',10,18),(1935,'Sonic Arts',70,7,'R24',5,19),(1936,'Arts & Theatre Management   ',70,7,'R25',6,20),(1937,'Design for Games & Gamification',67,7,'R35',12,17),(1938,'Design for User Experience',75,7,'R36',16,20),(1939,'Diploma In Pharmaceutical Science',83,30,'C65',5,10),(1940,'Diploma In Applied Chemistry',46,30,'C45',5,11),(1941,'Diploma In Food Science & Nutrition',68,30,'C69',4,13),(1942,'Diploma In Biologics & Process Technology',46,30,'C49',6,12),(1943,'Diploma In Chemical & Pharmaceutical Technology',112,30,'C73',9,15),(1944,'Diploma In Food & Beverage Business',65,31,'C46',6,16),(1945,'Diploma In Business Management',254,31,'C94',8,16),(1946,'Common Business Programme',255,31,'C34',7,16),(1947,'Diploma In Banking And Finance',65,31,'C96',7,13),(1948,'Diploma In Sport & Wellness Management',45,31,'C81',7,15),(1949,'Diploma In Accountancy & Finance',69,31,'C98',7,12),(1950,'Diploma In Hospitality & Tourism Management',56,31,'C67',9,17),(1951,'Diploma In Mass Media Management',50,31,'C93',9,12),(1952,'Diploma In Architecture',50,32,'C38',8,15),(1953,'Diploma In Visual Communication',68,32,'C63',5,15),(1954,'Diploma In Experiential Product & Interior Design',105,32,'C32',9,17),(1955,'Diploma In Digital Game Art & Design',66,32,'C60',10,14),(1956,'Diploma In Interaction Design',50,32,'C59',9,17),(1957,'Diploma In Motion Graphics Design',50,32,'C66',10,14),(1958,'Diploma In Animation & Visual Effects',113,32,'C33',5,12),(1959,'Diploma In Game Development & Technology',86,32,'C70',0,0),(1960,'Diploma In Advanced & Digital Manufacturing',64,33,'C62',0,0),(1961,'Common Engineering Programme',424,33,'C42',6,26),(1962,'Diploma In Engineering With Business',41,33,'C41',8,14),(1963,'Diploma In Nanotechnology & Materials Science',40,33,'C50',7,14),(1964,'Diploma In Robotics & Mechatronics',64,33,'C87',8,23),(1965,'Diploma In Biomedical Engineering',40,33,'C71',9,13),(1966,'Diploma In Aeronautical & Aerospace Technology',41,33,'C51',5,16),(1967,'Diploma In Aerospace Systems & Management',41,33,'C52',8,19),(1968,'Diploma In Electronic & Computer Engineering',83,33,'C89',6,18),(1969,'Diploma In Infocomm & Media Engineering',130,33,'C75',11,22),(1970,'Diploma In Ai & Data Engineering',40,33,'C31',0,0),(1971,'Diploma In Social Work',45,34,'C47',4,9),(1972,'Diploma In Oral Health Therapy',25,35,'C72',8,11),(1973,'Diploma In Nursing',800,35,'C97',5,28),(1974,'Diploma In Business Intelligence & Analytics',55,35,'C43',6,11),(1975,'Common Ict Programme',142,35,'C36',4,15),(1976,'Diploma In Infocomm & Security',64,35,'C80',9,16),(1977,'Diploma In Business & Financial Technology',86,35,'C35',10,15),(1978,'Diploma In Cybersecurity & Digital Forensics',75,35,'C54',3,9),(1979,'Diploma In Information Technology',102,35,'C85',6,14);
UNLOCK TABLES;

LOCK TABLES `scholarship` WRITE;
INSERT INTO `scholarship` VALUES (1,'Temasek Polytechnic Scholarship\r'),(2,'CSIT Diploma Scholarship\r'),(3,'PUB Sponsorship\r'),(4,'Singtel Engineering Cadet Scholarship Program\r'),(5,'Singtel Cyber Security Scholarship Program\r'),(6,'Temasek Polytechnic Foundation Programme Scholarship\r'),(7,'Freshman Scholarship\r'),(8,'PFP Scholarship\r'),(9,'NYP Industry Scholarship\r'),(10,'Daisy Phay-NYP Foundation Scholarship\r'),(11,'CSIT Diploma Scholarship\r'),(12,'NYP Scholarship (\'O\' Level Pathway)\r'),(13,'NYP Scholarship (PFP Pathway)\r'),(14,'SP Engineering Scholarship\r'),(15,'IMDA Infocomm Polytechnic Scholarship\r'),(16,'GAC Singaproe - MaritimeONE Scholarship\r'),(17,'DSTA Polytechnic Scholarship\r'),(18,'Zalora Scholarship\r'),(19,'Polytechnic Foundation Programme Study Award\r'),(20,'Donor Scholarship\r'),(21,'NP Scholarship\r');
UNLOCK TABLES;

LOCK TABLES `criteria` WRITE;
INSERT INTO `criteria` VALUES (1,'Singapore Citizen\r'),(2,'Singapore Permenant Resident\r'),(3,'Cumulative grade point average (CGPA) of >= 3.8 at the end of the second semester in Year 1\r'),(4,'Not in receipt of any other scholarships/sponsorships\r'),(5,' Net score of <= 10 points (ELR2B2) in the GCE ‘O’ Level Exam\r'),(6,' Net aggregate of <= 7 points (ELMAB3) in the GCE N(A) Level Exam\r'),(7,'top 5% of their diploma course cohort after their year 1 Semester 1 examinations\r'),(8,'good co-curricular activities records\r'),(9,'Not be a ZALORA employee or the immediate family member of a ZALORA employee\r'),(10,'Year 1 Students\r'),(11,'cGPA >= 3.50\r'),(12,'Freshmen from Diploma in Environmental & Water Technology Course\r'),(13,'Passion to work in industry\r'),(14,'Min CPGA 3.0\r'),(15,'Not financially sponsored by employers \r'),(16,'Good character and conduct\r'),(17,'Outstanding ELMAB3* at GCE N-Level examinations\r'),(18,'ELR2B2 raw score <= 12 in the O-Level exam\r'),(19,'enrolled into any RP full-time diploma via your top 3 choices\r'),(20,' Current N level student\r'),(21,' Have ELMAB3 raw score <= 10 for N-Level prelim exam\r'),(22,'ELR2B2 <= 10 in the GCE \'N\' Level exams\r'),(23,'Strong leadership qualities and potential\r'),(24,'Scholarship recipients (for awards that cover tuition fee only) are now allowed to hold a government-funded bursary concurrently\r'),(25,'set by individual donor\r');
UNLOCK TABLES; 

LOCK TABLES `scholarship_criteria` WRITE;
INSERT INTO `scholarship_criteria` VALUES (1,1,10),(2,1,7),(3,1,4),(4,2,1),(5,2,5),(6,3,12),(7,3,1),(8,3,2),(9,3,13),(10,4,10),(11,4,14),(12,5,10),(13,5,14),(14,6,17),(15,6,16),(16,6,15),(17,7,18),(18,7,19),(19,8,1),(20,8,2),(21,8,20),(22,8,21),(23,8,8),(24,9,1),(25,9,2),(26,9,3),(27,9,4),(28,10,1),(29,10,2),(30,10,4),(31,11,1),(32,11,5),(33,12,1),(34,12,2),(35,12,4),(36,12,5),(37,13,1),(38,13,2),(39,13,4),(40,13,6),(41,14,1),(42,14,2),(43,14,7),(44,14,8),(45,15,1),(46,15,8),(47,15,5),(48,16,1),(49,16,2),(50,16,5),(51,16,8),(52,17,1),(53,17,5),(54,17,8),(55,18,5),(56,18,8),(57,18,9),(58,19,5),(59,19,23),(60,19,24),(61,20,8),(62,20,23),(63,20,25),(64,21,22),(65,21,23),(66,21,8);
UNLOCK TABLES;

LOCK TABLES `school_scholarship` WRITE;
INSERT INTO `school_scholarship` VALUES (255,8,1),(256,9,1),(257,13,1),(258,11,1),(259,12,1),(260,10,1),(261,12,2),(262,10,2),(263,10,3),(264,10,4),(265,12,5),(266,8,6),(267,9,6),(268,13,6),(269,11,6),(270,12,6),(271,10,6),(272,1,7),(273,2,7),(274,3,7),(275,4,7),(276,6,7),(277,5,7),(278,7,7),(279,1,8),(280,2,8),(281,3,8),(282,4,8),(283,6,8),(284,5,8),(285,7,8),(286,30,9),(287,31,9),(288,32,9),(289,33,9),(290,34,9),(291,35,9),(292,30,10),(293,35,11),(294,30,12),(295,31,12),(296,32,12),(297,33,12),(298,34,12),(299,35,12),(300,30,13),(301,31,13),(302,32,13),(303,33,13),(304,34,13),(305,35,13),(306,17,14),(307,19,15),(308,20,16),(309,17,17),(310,15,18),(311,16,18),(312,14,18),(313,19,18),(314,17,18),(315,21,18),(316,20,18),(317,26,19),(318,23,19),(319,22,19),(320,24,19),(321,27,19),(322,28,19),(323,25,19),(324,29,20),(325,23,20),(326,22,20),(327,24,20),(328,26,20),(329,27,20),(330,28,20),(331,25,20),(332,27,21),(333,23,21),(334,22,21),(335,24,21),(336,26,21),(337,28,21),(338,25,21);
UNLOCK TABLES;
