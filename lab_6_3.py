from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker


class REGION:
    def __init__(self, params):
        self.name = params[0]
        self.population = params[1]
        self.square = params[2]
        self.city_list = params[3]

    def __repr__(self):
        return 'Name: {}\n' \
               'Population: {}\n' \
               'Square: {}\n' \
               'Big cities: {}\n'.format(self.name, self.population, self.square, '\t'.join(self.city_list))

    def belonging(self, city_to_find):
        if city_to_find in self.city_list:
            return True
        else:
            return False

    def population_density(self):
        return '{.2f}'.format(self.population / self.square)


# database declaration
Base = declarative_base()
engine = create_engine('mysql+pymysql://lab_6:lab_6@localhost:3306/lab_6', pool_recycle=3600, encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()


class Region(Base):
    __tablename__ = 'regions'
    region_id = Column(Integer(), primary_key=True)
    region_name = Column(String(50), nullable=False)
    region_population = Column(Integer(), nullable=False)
    region_square = Column(Integer, nullable=False)


class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer(), primary_key=True)
    city_name = Column(String(20), nullable=False)
    region_id = Column(Integer(), ForeignKey('regions.region_id'), nullable=False)
    region = relationship('Region', backref=backref('regions'), order_by=city_id)


def add_region():
    while True:
        try:
            region_name = input('Type region name: ')
            population = int(input('Type region population: '))
            assert population > 0
            square = int(input('Type region square: '))
            assert square > 0
        except AssertionError:
            print('Your data seems to be not real, try again.'
                  ' Remember that population and square should be more than 0')
        except ValueError:
            print('Your input is incorrect, try again')
        new_region = Region(region_name=region_name,
                            region_population=population,
                            region_square=square)
        session.add(new_region)
        session.commit()
        reg_id = session.query(Region.region_name,Region.region_id).filter(Region.region_name == region_name).first()
        reg_id = reg_id.region_id
        while True:
            a = input('Type name of a city (\'stop\' to stop')
            if a == 'stop':
                break
            else:
                new_city = City(city_name=a,
                                region_id=reg_id)
                session.add(new_city)
                session.commit()
        print('Region \'{}\' added'.format(region_name))
        break
    return


def add_city():
    print('Regions:')
    tmp_regions = session.query(Region).all()
    for i in tmp_regions:
        print("{}. {}".format(i.region_id, i.region_name))
    try:
        chosen_region = int(input('Choose a region to add a city (type number of chosen region) '))
        new_city_name = input('Type name of the city ')
        reg_id = session.query(Region).filter(Region.region_id == chosen_region).first().region_id
        new_city = City(city_name=new_city_name,
                        region_id=reg_id)
        session.add(new_city)
        session.commit()
    except ValueError:
        print('input data incorrect')

    return


def edit_region():
    tmp_regions = session.query(Region).all()
    for i in tmp_regions:
        print('{}. {}'.format(i.region_id, i.region_name))


def edit_city():
    pass


def delete_region():
    pass


def delete_city():
    pass


# main body
Base.metadata.create_all(engine)  # creating tables from schema(no affect if tables already exist)
my_help = 'Laboratory work #6\n'\
        'Made by Oleksandr Korienev, student of iv-72\n'\
        'Only English is supported, cyrillic symbols can cause a crash\n'\
        'available commands:\n'\
        '\'add_region\' to add new region to the database\n'\
        '\'add_city\' to add new city to the database\n'\
        '\'edit_region\' to edit region \n'\
        '\'edit_city\' to edit city\n'\
        '\'delete_region\' to delete region from database (deleting region will cause deleting'\
        'all cities which are linked to it!)\n'\
        '\'delete_city\' to delete city from the database\n'\
        '\'exit\' to finish the work'

while True:
    main_choice = input('choose an option, \'help\' to display help')
    if main_choice == 'add_region':
        add_region()
    elif main_choice == 'help':
        print(my_help)
    elif main_choice == 'add_city':
        add_city()
    elif main_choice == 'edit_region':
        edit_region()
    elif main_choice == exit:
        break

region_objects_list = []
regions = session.query(Region).all()
raw_region_list = [[i.region_id, i.region_name, i.region_population, i.region_square] for i in regions]
for i in raw_region_list:
    city_query = session.query(City).filter(City.region_id == i[0]).all()
    tmp_cities = [j.city_name for j in city_query]
    i.append(tmp_cities)
    region_objects_list.append(REGION(i[1:]))
print(my_help)
