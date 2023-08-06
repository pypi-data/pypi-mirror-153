# auto-generated content
from collections import OrderedDict
from enum import Enum
from pkgutil import extend_path


__path__ = extend_path(__path__, __name__)
SCHEMA_VERSION = '7.11.0'
NESTED_SEARCHABLE_KEYS = [
    'otherSites',
    'inputs',
    'emissions',
    'products',
    'practices',
    'transformations',
    'emissionsResourceUse',
    'impacts',
    'endpoints',
    'metaAnalyses',
    'synonyms',
    'subClassOf',
    'defaultProperties'
]


class NodeType(Enum):
    ACTOR = 'Actor'
    CYCLE = 'Cycle'
    IMPACTASSESSMENT = 'ImpactAssessment'
    ORGANISATION = 'Organisation'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'


class SchemaType(Enum):
    ACTOR = 'Actor'
    BIBLIOGRAPHY = 'Bibliography'
    COMPLETENESS = 'Completeness'
    CYCLE = 'Cycle'
    EMISSION = 'Emission'
    IMPACTASSESSMENT = 'ImpactAssessment'
    INDICATOR = 'Indicator'
    INFRASTRUCTURE = 'Infrastructure'
    INPUT = 'Input'
    MEASUREMENT = 'Measurement'
    ORGANISATION = 'Organisation'
    PRACTICE = 'Practice'
    PRODUCT = 'Product'
    PROPERTY = 'Property'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'
    TRANSFORMATION = 'Transformation'


NODE_TYPES = [e.value for e in NodeType]
SCHEMA_TYPES = [e.value for e in SchemaType]


def is_node_type(type: str): return type in NODE_TYPES


def is_type_valid(type: str): return type in SCHEMA_TYPES


def is_schema_type(type: str): return is_type_valid(type) and not is_node_type(type)


class Actor:
    def __init__(self):
        self.required = [
            'lastName',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.ACTOR.value
        self.fields['name'] = ''
        self.fields['firstName'] = ''
        self.fields['lastName'] = ''
        self.fields['orcid'] = ''
        self.fields['scopusID'] = ''
        self.fields['primaryInstitution'] = ''
        self.fields['city'] = ''
        self.fields['country'] = None
        self.fields['email'] = ''
        self.fields['website'] = None
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Bibliography:
    def __init__(self):
        self.required = [
            'name',
            'title',
            'authors',
            'outlet',
            'year'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.BIBLIOGRAPHY.value
        self.fields['name'] = ''
        self.fields['documentDOI'] = ''
        self.fields['title'] = ''
        self.fields['arxivID'] = ''
        self.fields['scopus'] = ''
        self.fields['mendeleyID'] = ''
        self.fields['authors'] = []
        self.fields['outlet'] = ''
        self.fields['year'] = None
        self.fields['volume'] = None
        self.fields['issue'] = ''
        self.fields['chapter'] = ''
        self.fields['pages'] = ''
        self.fields['publisher'] = ''
        self.fields['city'] = ''
        self.fields['editors'] = []
        self.fields['institutionPub'] = []
        self.fields['websites'] = []
        self.fields['articlePdf'] = ''
        self.fields['dateAccessed'] = []
        self.fields['abstract'] = ''
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Completeness:
    def __init__(self):
        self.required = [
            'electricityFuel',
            'material',
            'fertilizer',
            'soilAmendments',
            'pesticidesAntibiotics',
            'water',
            'animalFeed',
            'other',
            'products',
            'cropResidue',
            'excretaManagement'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.COMPLETENESS.value
        self.fields['electricityFuel'] = False
        self.fields['material'] = False
        self.fields['fertilizer'] = False
        self.fields['soilAmendments'] = False
        self.fields['pesticidesAntibiotics'] = False
        self.fields['water'] = False
        self.fields['animalFeed'] = False
        self.fields['other'] = False
        self.fields['products'] = False
        self.fields['cropResidue'] = False
        self.fields['excretaManagement'] = False
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CycleStartDateDefinition(Enum):
    HARVEST_OF_PREVIOUS_CROP = 'harvest of previous crop'
    SOIL_PREPARATION_DATE = 'soil preparation date'
    SOWING_DATE = 'sowing date'
    START_OF_YEAR = 'start of year'
    STOCKING_DATE = 'stocking date'


class CycleFunctionalUnit(Enum):
    _1_HA = '1 ha'
    RELATIVE = 'relative'


class Cycle:
    def __init__(self):
        self.required = [
            'site',
            'endDate',
            'functionalUnit',
            'dataCompleteness',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.CYCLE.value
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['treatment'] = ''
        self.fields['dataDescription'] = ''
        self.fields['site'] = None
        self.fields['otherSites'] = []
        self.fields['siteDuration'] = None
        self.fields['otherSitesDuration'] = None
        self.fields['harvestedArea'] = None
        self.fields['defaultSource'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['startDateDefinition'] = ''
        self.fields['cycleDuration'] = None
        self.fields['functionalUnit'] = ''
        self.fields['functionalUnitDetails'] = ''
        self.fields['numberOfCycles'] = None
        self.fields['dataCompleteness'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['transformations'] = []
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class EmissionStatsDefinition(Enum):
    CYCLES = 'cycles'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class EmissionMethodTier(Enum):
    BACKGROUND = 'background'
    MEASURED = 'measured'
    TIER_1 = 'tier 1'
    TIER_2 = 'tier 2'
    TIER_3 = 'tier 3'


class Emission:
    def __init__(self):
        self.required = [
            'term',
            'value',
            'methodModel',
            'methodTier'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.EMISSION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['emissionDuration'] = None
        self.fields['depth'] = None
        self.fields['properties'] = []
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['methodTier'] = ''
        self.fields['inputs'] = []
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None
        self.fields['deleted'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ImpactAssessmentAllocationMethod(Enum):
    ECONOMIC = 'economic'
    ENERGY = 'energy'
    MASS = 'mass'
    NONE = 'none'
    NONEREQUIRED = 'noneRequired'
    SYSTEMEXPANSION = 'systemExpansion'


class ImpactAssessment:
    def __init__(self):
        self.required = [
            'endDate',
            'country',
            'product',
            'functionalUnitQuantity',
            'allocationMethod',
            'systemBoundary',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.IMPACTASSESSMENT.value
        self.fields['name'] = ''
        self.fields['version'] = ''
        self.fields['versionDetails'] = ''
        self.fields['organisation'] = None
        self.fields['cycle'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['site'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['product'] = None
        self.fields['functionalUnitQuantity'] = 1
        self.fields['allocationMethod'] = ''
        self.fields['systemBoundary'] = False
        self.fields['source'] = None
        self.fields['emissionsResourceUse'] = []
        self.fields['impacts'] = []
        self.fields['endpoints'] = []
        self.fields['organic'] = False
        self.fields['irrigated'] = False
        self.fields['autoGenerated'] = False
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class IndicatorStatsDefinition(Enum):
    CYCLES = 'cycles'
    IMPACTASSESSMENTS = 'impactAssessments'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class Indicator:
    def __init__(self):
        self.required = [
            'term',
            'value'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.INDICATOR.value
        self.fields['term'] = None
        self.fields['value'] = None
        self.fields['distribution'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['inputs'] = []
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InfrastructureOwnershipStatus(Enum):
    BORROWED = 'borrowed'
    OWNED = 'owned'
    RENTED = 'rented'


class Infrastructure:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.INFRASTRUCTURE.value
        self.fields['term'] = None
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['lifespan'] = None
        self.fields['lifespanHours'] = None
        self.fields['mass'] = None
        self.fields['area'] = None
        self.fields['ownershipStatus'] = ''
        self.fields['inputs'] = []
        self.fields['impactAssessment'] = None
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InputStatsDefinition(Enum):
    CYCLES = 'cycles'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class Input:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.INPUT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['inputDuration'] = None
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['currency'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['operation'] = None
        self.fields['country'] = None
        self.fields['impactAssessment'] = None
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class MeasurementStatsDefinition(Enum):
    CYCLES = 'cycles'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class Measurement:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.MEASUREMENT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurementDuration'] = None
        self.fields['depthUpper'] = None
        self.fields['depthLower'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['properties'] = []
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Organisation:
    def __init__(self):
        self.required = [
            'country',
            'uploadBy',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.ORGANISATION.value
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['streetAddress'] = ''
        self.fields['city'] = ''
        self.fields['region'] = None
        self.fields['country'] = None
        self.fields['postOfficeBoxNumber'] = ''
        self.fields['postalCode'] = ''
        self.fields['website'] = None
        self.fields['glnNumber'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['originalId'] = ''
        self.fields['uploadBy'] = None
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PracticeStatsDefinition(Enum):
    CYCLES = 'cycles'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class PracticeOwnershipStatus(Enum):
    BORROWED = 'borrowed'
    OWNED = 'owned'
    RENTED = 'rented'


class Practice:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PRACTICE.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['currency'] = ''
        self.fields['ownershipStatus'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ProductStatsDefinition(Enum):
    CYCLES = 'cycles'
    MODELLED = 'modelled'
    ORGANISATIONS = 'organisations'
    OTHEROBSERVATIONS = 'otherObservations'
    REGIONS = 'regions'
    REPLICATIONS = 'replications'
    SIMULATED = 'simulated'
    SITES = 'sites'
    SPATIAL = 'spatial'
    TIME = 'time'


class Product:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PRODUCT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['variety'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['price'] = None
        self.fields['revenue'] = None
        self.fields['currency'] = ''
        self.fields['economicValueShare'] = None
        self.fields['primary'] = False
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PropertyStatsDefinition(Enum):
    MODELLED = 'modelled'
    OBSERVATIONS = 'observations'
    REGIONS = 'regions'
    SIMULATED = 'simulated'
    SPATIAL = 'spatial'


class Property:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.PROPERTY.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SiteSiteType(Enum):
    AGRI_FOOD_PROCESSOR = 'agri-food processor'
    ANIMAL_HOUSING = 'animal housing'
    CROPLAND = 'cropland'
    FOOD_RETAILER = 'food retailer'
    FOREST = 'forest'
    LAKE = 'lake'
    OTHER_NATURAL_VEGETATION = 'other natural vegetation'
    PERMANENT_PASTURE = 'permanent pasture'
    POND = 'pond'
    RIVER_OR_STREAM = 'river or stream'
    SEA_OR_OCEAN = 'sea or ocean'


class SiteTenure(Enum):
    FARMING_ON_COMMON_LAND = 'farming on common land'
    FARMING_ON_OWNED_LAND = 'farming on owned land'
    FARMING_ON_RENTED_LAND = 'farming on rented land'
    OTHER_TENURE_MODEL = 'other tenure model'
    SHARE_FARMING = 'share farming'


class Site:
    def __init__(self):
        self.required = [
            'siteType',
            'country',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.SITE.value
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['siteType'] = ''
        self.fields['organisation'] = None
        self.fields['tenure'] = ''
        self.fields['defaultSource'] = None
        self.fields['numberOfSites'] = None
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['areaSd'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['ecoregion'] = ''
        self.fields['awareWaterBasinId'] = ''
        self.fields['glnNumber'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurements'] = []
        self.fields['infrastructure'] = []
        self.fields['practices'] = []
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Source:
    def __init__(self):
        self.required = [
            'name',
            'bibliography',
            'uploadBy',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.SOURCE.value
        self.fields['name'] = ''
        self.fields['bibliography'] = None
        self.fields['metaAnalyses'] = []
        self.fields['doiHESTIA'] = ''
        self.fields['uploadDate'] = None
        self.fields['uploadBy'] = None
        self.fields['uploadNotes'] = ''
        self.fields['validationDate'] = None
        self.fields['validationBy'] = []
        self.fields['intendedApplication'] = ''
        self.fields['studyReasons'] = ''
        self.fields['intendedAudience'] = ''
        self.fields['comparativeAssertions'] = False
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class TermTermType(Enum):
    ANIMALMANAGEMENT = 'animalManagement'
    ANIMALPRODUCT = 'animalProduct'
    ANTIBIOTIC = 'antibiotic'
    AQUACULTUREMANAGEMENT = 'aquacultureManagement'
    BIODIVERSITY = 'biodiversity'
    BUILDING = 'building'
    CHARACTERISEDINDICATOR = 'characterisedIndicator'
    CROP = 'crop'
    CROPESTABLISHMENT = 'cropEstablishment'
    CROPPROTECTION = 'cropProtection'
    CROPRESIDUE = 'cropResidue'
    CROPRESIDUEMANAGEMENT = 'cropResidueManagement'
    CROPSUPPORT = 'cropSupport'
    ELECTRICITY = 'electricity'
    EMISSION = 'emission'
    ENDPOINTINDICATOR = 'endpointIndicator'
    EXCRETA = 'excreta'
    EXCRETAMANAGEMENT = 'excretaManagement'
    FUEL = 'fuel'
    INORGANICFERTILIZER = 'inorganicFertilizer'
    IRRIGATION = 'irrigation'
    LANDUSEMANAGEMENT = 'landUseManagement'
    LIVEANIMAL = 'liveAnimal'
    LIVEAQUATICSPECIES = 'liveAquaticSpecies'
    MACHINERY = 'machinery'
    MATERIAL = 'material'
    MEASUREMENT = 'measurement'
    METHODEMISSIONRESOURCEUSE = 'methodEmissionResourceUse'
    METHODMEASUREMENT = 'methodMeasurement'
    MODEL = 'model'
    OPERATION = 'operation'
    ORGANICFERTILIZER = 'organicFertilizer'
    OTHER = 'other'
    PESTICIDEAI = 'pesticideAI'
    PESTICIDEBRANDNAME = 'pesticideBrandName'
    PROCESSEDFOOD = 'processedFood'
    PROPERTY = 'property'
    REGION = 'region'
    RESOURCEUSE = 'resourceUse'
    SOILAMENDMENT = 'soilAmendment'
    SOILTEXTURE = 'soilTexture'
    SOILTYPE = 'soilType'
    STANDARDSLABELS = 'standardsLabels'
    SYSTEM = 'system'
    TILLAGE = 'tillage'
    TRANSPORT = 'transport'
    USDASOILTYPE = 'usdaSoilType'
    WATER = 'water'
    WATERREGIME = 'waterRegime'


class Term:
    def __init__(self):
        self.required = [
            'name',
            'termType'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = NodeType.TERM.value
        self.fields['name'] = ''
        self.fields['synonyms'] = []
        self.fields['definition'] = ''
        self.fields['description'] = ''
        self.fields['units'] = ''
        self.fields['subClassOf'] = []
        self.fields['defaultProperties'] = []
        self.fields['casNumber'] = ''
        self.fields['ecoinventActivityId'] = ''
        self.fields['fishstatName'] = ''
        self.fields['hsCode'] = ''
        self.fields['iccCode'] = None
        self.fields['iso31662Code'] = ''
        self.fields['gadmFullName'] = ''
        self.fields['gadmId'] = ''
        self.fields['gadmLevel'] = None
        self.fields['gadmName'] = ''
        self.fields['gadmCountry'] = ''
        self.fields['gtin'] = ''
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['area'] = None
        self.fields['openLCAId'] = ''
        self.fields['scientificName'] = ''
        self.fields['website'] = None
        self.fields['agrovoc'] = None
        self.fields['aquastatSpeciesFactSheet'] = None
        self.fields['chemidplus'] = None
        self.fields['feedipedia'] = None
        self.fields['fishbase'] = None
        self.fields['pubchem'] = None
        self.fields['wikipedia'] = None
        self.fields['termType'] = ''
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class Transformation:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['type'] = SchemaType.TRANSFORMATION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['transformationDuration'] = None
        self.fields['previousTransformationTerm'] = None
        self.fields['previousTransformationShare'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ActorJSONLD:
    def __init__(self):
        self.required = [
            'lastName',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.ACTOR.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['firstName'] = ''
        self.fields['lastName'] = ''
        self.fields['orcid'] = ''
        self.fields['scopusID'] = ''
        self.fields['primaryInstitution'] = ''
        self.fields['city'] = ''
        self.fields['country'] = None
        self.fields['email'] = ''
        self.fields['website'] = None
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class BibliographyJSONLD:
    def __init__(self):
        self.required = [
            'name',
            'title',
            'authors',
            'outlet',
            'year'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.BIBLIOGRAPHY.value
        self.fields['name'] = ''
        self.fields['documentDOI'] = ''
        self.fields['title'] = ''
        self.fields['arxivID'] = ''
        self.fields['scopus'] = ''
        self.fields['mendeleyID'] = ''
        self.fields['authors'] = []
        self.fields['outlet'] = ''
        self.fields['year'] = None
        self.fields['volume'] = None
        self.fields['issue'] = ''
        self.fields['chapter'] = ''
        self.fields['pages'] = ''
        self.fields['publisher'] = ''
        self.fields['city'] = ''
        self.fields['editors'] = []
        self.fields['institutionPub'] = []
        self.fields['websites'] = []
        self.fields['articlePdf'] = ''
        self.fields['dateAccessed'] = []
        self.fields['abstract'] = ''
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CompletenessJSONLD:
    def __init__(self):
        self.required = [
            'electricityFuel',
            'material',
            'fertilizer',
            'soilAmendments',
            'pesticidesAntibiotics',
            'water',
            'animalFeed',
            'other',
            'products',
            'cropResidue',
            'excretaManagement'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.COMPLETENESS.value
        self.fields['electricityFuel'] = False
        self.fields['material'] = False
        self.fields['fertilizer'] = False
        self.fields['soilAmendments'] = False
        self.fields['pesticidesAntibiotics'] = False
        self.fields['water'] = False
        self.fields['animalFeed'] = False
        self.fields['other'] = False
        self.fields['products'] = False
        self.fields['cropResidue'] = False
        self.fields['excretaManagement'] = False
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class CycleJSONLD:
    def __init__(self):
        self.required = [
            'site',
            'endDate',
            'functionalUnit',
            'dataCompleteness',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.CYCLE.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['treatment'] = ''
        self.fields['dataDescription'] = ''
        self.fields['site'] = None
        self.fields['otherSites'] = []
        self.fields['siteDuration'] = None
        self.fields['otherSitesDuration'] = None
        self.fields['harvestedArea'] = None
        self.fields['defaultSource'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['startDateDefinition'] = ''
        self.fields['cycleDuration'] = None
        self.fields['functionalUnit'] = ''
        self.fields['functionalUnitDetails'] = ''
        self.fields['numberOfCycles'] = None
        self.fields['dataCompleteness'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['transformations'] = []
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class EmissionJSONLD:
    def __init__(self):
        self.required = [
            'term',
            'value',
            'methodModel',
            'methodTier'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.EMISSION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['emissionDuration'] = None
        self.fields['depth'] = None
        self.fields['properties'] = []
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['methodTier'] = ''
        self.fields['inputs'] = []
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None
        self.fields['deleted'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ImpactAssessmentJSONLD:
    def __init__(self):
        self.required = [
            'endDate',
            'country',
            'product',
            'functionalUnitQuantity',
            'allocationMethod',
            'systemBoundary',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.IMPACTASSESSMENT.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['version'] = ''
        self.fields['versionDetails'] = ''
        self.fields['organisation'] = None
        self.fields['cycle'] = None
        self.fields['endDate'] = ''
        self.fields['startDate'] = ''
        self.fields['site'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['product'] = None
        self.fields['functionalUnitQuantity'] = 1
        self.fields['allocationMethod'] = ''
        self.fields['systemBoundary'] = False
        self.fields['source'] = None
        self.fields['emissionsResourceUse'] = []
        self.fields['impacts'] = []
        self.fields['endpoints'] = []
        self.fields['organic'] = False
        self.fields['irrigated'] = False
        self.fields['autoGenerated'] = False
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class IndicatorJSONLD:
    def __init__(self):
        self.required = [
            'term',
            'value'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.INDICATOR.value
        self.fields['term'] = None
        self.fields['value'] = None
        self.fields['distribution'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['inputs'] = []
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InfrastructureJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.INFRASTRUCTURE.value
        self.fields['term'] = None
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['lifespan'] = None
        self.fields['lifespanHours'] = None
        self.fields['mass'] = None
        self.fields['area'] = None
        self.fields['ownershipStatus'] = ''
        self.fields['inputs'] = []
        self.fields['impactAssessment'] = None
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class InputJSONLD:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.INPUT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['inputDuration'] = None
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['currency'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['operation'] = None
        self.fields['country'] = None
        self.fields['impactAssessment'] = None
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class MeasurementJSONLD:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.MEASUREMENT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurementDuration'] = None
        self.fields['depthUpper'] = None
        self.fields['depthLower'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['properties'] = []
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class OrganisationJSONLD:
    def __init__(self):
        self.required = [
            'country',
            'uploadBy',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.ORGANISATION.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['streetAddress'] = ''
        self.fields['city'] = ''
        self.fields['region'] = None
        self.fields['country'] = None
        self.fields['postOfficeBoxNumber'] = ''
        self.fields['postalCode'] = ''
        self.fields['website'] = None
        self.fields['glnNumber'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['originalId'] = ''
        self.fields['uploadBy'] = None
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PracticeJSONLD:
    def __init__(self):
        self.required = []
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PRACTICE.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['currency'] = ''
        self.fields['ownershipStatus'] = ''
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class ProductJSONLD:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PRODUCT.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['variety'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['dates'] = None
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['price'] = None
        self.fields['revenue'] = None
        self.fields['currency'] = ''
        self.fields['economicValueShare'] = None
        self.fields['primary'] = False
        self.fields['properties'] = []
        self.fields['reliability'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class PropertyJSONLD:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.PROPERTY.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['min'] = None
        self.fields['max'] = None
        self.fields['statsDefinition'] = ''
        self.fields['observations'] = None
        self.fields['methodModel'] = None
        self.fields['methodModelDescription'] = ''
        self.fields['source'] = None
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = None
        self.fields['aggregatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SiteJSONLD:
    def __init__(self):
        self.required = [
            'siteType',
            'country',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.SITE.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['description'] = ''
        self.fields['siteType'] = ''
        self.fields['organisation'] = None
        self.fields['tenure'] = ''
        self.fields['defaultSource'] = None
        self.fields['numberOfSites'] = None
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['areaSd'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['country'] = None
        self.fields['region'] = None
        self.fields['ecoregion'] = ''
        self.fields['awareWaterBasinId'] = ''
        self.fields['glnNumber'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['measurements'] = []
        self.fields['infrastructure'] = []
        self.fields['practices'] = []
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None
        self.fields['aggregated'] = False
        self.fields['aggregatedVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class SourceJSONLD:
    def __init__(self):
        self.required = [
            'name',
            'bibliography',
            'uploadBy',
            'dataPrivate'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.SOURCE.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['bibliography'] = None
        self.fields['metaAnalyses'] = []
        self.fields['doiHESTIA'] = ''
        self.fields['uploadDate'] = None
        self.fields['uploadBy'] = None
        self.fields['uploadNotes'] = ''
        self.fields['validationDate'] = None
        self.fields['validationBy'] = []
        self.fields['intendedApplication'] = ''
        self.fields['studyReasons'] = ''
        self.fields['intendedAudience'] = ''
        self.fields['comparativeAssertions'] = False
        self.fields['originalId'] = ''
        self.fields['schemaVersion'] = ''
        self.fields['dataPrivate'] = False

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class TermJSONLD:
    def __init__(self):
        self.required = [
            'name',
            'termType'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = NodeType.TERM.value
        self.fields['@id'] = ''
        self.fields['name'] = ''
        self.fields['synonyms'] = []
        self.fields['definition'] = ''
        self.fields['description'] = ''
        self.fields['units'] = ''
        self.fields['subClassOf'] = []
        self.fields['defaultProperties'] = []
        self.fields['casNumber'] = ''
        self.fields['ecoinventActivityId'] = ''
        self.fields['fishstatName'] = ''
        self.fields['hsCode'] = ''
        self.fields['iccCode'] = None
        self.fields['iso31662Code'] = ''
        self.fields['gadmFullName'] = ''
        self.fields['gadmId'] = ''
        self.fields['gadmLevel'] = None
        self.fields['gadmName'] = ''
        self.fields['gadmCountry'] = ''
        self.fields['gtin'] = ''
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['area'] = None
        self.fields['openLCAId'] = ''
        self.fields['scientificName'] = ''
        self.fields['website'] = None
        self.fields['agrovoc'] = None
        self.fields['aquastatSpeciesFactSheet'] = None
        self.fields['chemidplus'] = None
        self.fields['feedipedia'] = None
        self.fields['fishbase'] = None
        self.fields['pubchem'] = None
        self.fields['wikipedia'] = None
        self.fields['termType'] = ''
        self.fields['schemaVersion'] = ''

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


class TransformationJSONLD:
    def __init__(self):
        self.required = [
            'term'
        ]
        self.fields = OrderedDict()
        self.fields['@type'] = SchemaType.TRANSFORMATION.value
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['startDate'] = ''
        self.fields['endDate'] = ''
        self.fields['transformationDuration'] = None
        self.fields['previousTransformationTerm'] = None
        self.fields['previousTransformationShare'] = None
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['schemaVersion'] = ''
        self.fields['added'] = None
        self.fields['addedVersion'] = None
        self.fields['updated'] = None
        self.fields['updatedVersion'] = None

    def to_dict(self):
        values = OrderedDict()
        for key, value in self.fields.items():
            if (value is not None and value != '' and value != []) or key in self.required:
                values[key] = value
        return values


ACTOR_COUNTRY = [
    TermTermType.REGION
]


EMISSION_TERM = [
    TermTermType.EMISSION,
    TermTermType.CHARACTERISEDINDICATOR,
    TermTermType.RESOURCEUSE
]


EMISSION_INPUTS = [
    TermTermType.ANTIBIOTIC,
    TermTermType.ELECTRICITY,
    TermTermType.FUEL,
    TermTermType.MATERIAL,
    TermTermType.INORGANICFERTILIZER,
    TermTermType.ORGANICFERTILIZER,
    TermTermType.PESTICIDEAI,
    TermTermType.PESTICIDEBRANDNAME,
    TermTermType.OTHER,
    TermTermType.SOILAMENDMENT,
    TermTermType.WATER,
    TermTermType.TRANSPORT,
    TermTermType.ANIMALPRODUCT,
    TermTermType.CROP,
    TermTermType.CROPRESIDUE,
    TermTermType.LIVEANIMAL,
    TermTermType.LIVEAQUATICSPECIES,
    TermTermType.PROCESSEDFOOD,
    TermTermType.EXCRETAMANAGEMENT,
    TermTermType.OPERATION
]


EMISSION_METHODMODEL = [
    TermTermType.MODEL,
    TermTermType.METHODEMISSIONRESOURCEUSE
]


IMPACTASSESSMENT_PRODUCT = [
    TermTermType.ANTIBIOTIC,
    TermTermType.ELECTRICITY,
    TermTermType.FUEL,
    TermTermType.MATERIAL,
    TermTermType.INORGANICFERTILIZER,
    TermTermType.ORGANICFERTILIZER,
    TermTermType.PESTICIDEAI,
    TermTermType.PESTICIDEBRANDNAME,
    TermTermType.OTHER,
    TermTermType.SOILAMENDMENT,
    TermTermType.WATER,
    TermTermType.ANIMALPRODUCT,
    TermTermType.CROP,
    TermTermType.CROPRESIDUE,
    TermTermType.EXCRETA,
    TermTermType.LIVEANIMAL,
    TermTermType.LIVEAQUATICSPECIES,
    TermTermType.PROCESSEDFOOD
]


IMPACTASSESSMENT_COUNTRY = [
    TermTermType.REGION
]


IMPACTASSESSMENT_REGION = [
    TermTermType.REGION
]


IMPACTASSESSMENT_EMISSIONSRESOURCEUSETERM = [
    TermTermType.CHARACTERISEDINDICATOR,
    TermTermType.EMISSION,
    TermTermType.RESOURCEUSE
]


IMPACTASSESSMENT_IMPACTSTERM = [
    TermTermType.CHARACTERISEDINDICATOR
]


IMPACTASSESSMENT_ENDPOINTSTERM = [
    TermTermType.ENDPOINTINDICATOR
]


INDICATOR_TERM = [
    TermTermType.EMISSION,
    TermTermType.ENDPOINTINDICATOR,
    TermTermType.CHARACTERISEDINDICATOR,
    TermTermType.RESOURCEUSE
]


INDICATOR_METHODMODEL = [
    TermTermType.MODEL,
    TermTermType.METHODEMISSIONRESOURCEUSE
]


INFRASTRUCTURE_TERM = [
    TermTermType.BUILDING,
    TermTermType.CROPPROTECTION,
    TermTermType.CROPSUPPORT,
    TermTermType.IRRIGATION,
    TermTermType.MACHINERY
]


INFRASTRUCTURE_INPUTSTERM = [
    TermTermType.ELECTRICITY,
    TermTermType.FUEL,
    TermTermType.MATERIAL,
    TermTermType.OTHER,
    TermTermType.TRANSPORT,
    TermTermType.WATER
]


INPUT_TERM = [
    TermTermType.ANTIBIOTIC,
    TermTermType.ELECTRICITY,
    TermTermType.FUEL,
    TermTermType.MATERIAL,
    TermTermType.INORGANICFERTILIZER,
    TermTermType.ORGANICFERTILIZER,
    TermTermType.PESTICIDEAI,
    TermTermType.PESTICIDEBRANDNAME,
    TermTermType.OTHER,
    TermTermType.SOILAMENDMENT,
    TermTermType.TRANSPORT,
    TermTermType.WATER,
    TermTermType.ANIMALPRODUCT,
    TermTermType.CROP,
    TermTermType.LIVEANIMAL,
    TermTermType.LIVEAQUATICSPECIES,
    TermTermType.EXCRETA,
    TermTermType.PROCESSEDFOOD
]


INPUT_METHODMODEL = [
    TermTermType.MODEL
]


INPUT_OPERATION = [
    TermTermType.OPERATION
]


INPUT_COUNTRY = [
    TermTermType.REGION
]


MEASUREMENT_TERM = [
    TermTermType.MEASUREMENT,
    TermTermType.SOILTEXTURE,
    TermTermType.SOILTYPE,
    TermTermType.USDASOILTYPE
]


MEASUREMENT_METHODMODEL = [
    TermTermType.METHODMEASUREMENT,
    TermTermType.MODEL
]


ORGANISATION_COUNTRY = [
    TermTermType.REGION
]


ORGANISATION_REGION = [
    TermTermType.REGION
]


PRACTICE_TERM = [
    TermTermType.ANIMALMANAGEMENT,
    TermTermType.AQUACULTUREMANAGEMENT,
    TermTermType.BIODIVERSITY,
    TermTermType.CROPESTABLISHMENT,
    TermTermType.CROPRESIDUEMANAGEMENT,
    TermTermType.EXCRETAMANAGEMENT,
    TermTermType.LANDUSEMANAGEMENT,
    TermTermType.STANDARDSLABELS,
    TermTermType.SYSTEM,
    TermTermType.TILLAGE,
    TermTermType.WATERREGIME,
    TermTermType.OPERATION
]


PRACTICE_METHODMODEL = [
    TermTermType.MODEL
]


PRODUCT_TERM = [
    TermTermType.ANIMALPRODUCT,
    TermTermType.CROP,
    TermTermType.CROPRESIDUE,
    TermTermType.ELECTRICITY,
    TermTermType.LIVEANIMAL,
    TermTermType.LIVEAQUATICSPECIES,
    TermTermType.EXCRETA,
    TermTermType.ORGANICFERTILIZER,
    TermTermType.PROCESSEDFOOD,
    TermTermType.OTHER
]


PRODUCT_METHODMODEL = [
    TermTermType.MODEL
]


PROPERTY_TERM = [
    TermTermType.PROPERTY
]


PROPERTY_METHODMODEL = [
    TermTermType.MODEL
]


SITE_COUNTRY = [
    TermTermType.REGION
]


SITE_REGION = [
    TermTermType.REGION
]


SITE_PRACTICESTERM = [
    TermTermType.BIODIVERSITY,
    TermTermType.CROPESTABLISHMENT,
    TermTermType.LANDUSEMANAGEMENT,
    TermTermType.STANDARDSLABELS,
    TermTermType.SYSTEM,
    TermTermType.WATERREGIME
]


TRANSFORMATION_TERM = [
    TermTermType.EXCRETAMANAGEMENT,
    TermTermType.OPERATION
]
