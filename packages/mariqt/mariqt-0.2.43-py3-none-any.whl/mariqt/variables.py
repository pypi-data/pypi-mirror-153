""" A dictionary holding various header field names to store 4.5D navigation information in the form of: t (utc time), x (longitude), y (latitude), z (depth: below sea level), a (altitude: above seafloor)"""
from enum import Enum
import os

myDir = os.path.dirname(os.path.abspath(__file__))
version = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"version.py")) as fp:
    exec(fp.read(), version)
	
version = version['__version__']

apis = {
		'osis_underway':'https://dm-apps-node0.geomar.de/osis-underway/api/v1/'
		}

pos_header = {
		# Field/column name definition for internally handling this kind of t,y,x,z,h position data
		"mariqt":{
			'utc':'utc',		# YYYY-MM-DD HH:ii:ss.sssss+0000 (UTC!!!) -> t-axis
			'lat':'lat',		# Decimal degrees, WGS84 / EPSG4362 -> y-axis
			'lon':'lon',		# Decimal degrees, WGS84 / EPSG4326 -> x-axis
			'dep':'dep',		# Depth of the signal, sample, platform, ... *in the water* -> z-axis, positive when submerged, negative when in air
			'hgt':'hgt',		# Height above the seafloor -> relative measure!
			'uncert':'uncert' 	# Coorindate uncertainty in standard deviation
		},

		# Definition of field/column names according to the iFDO specification:
		# https://gitlab.hzdr.de/datahub/marehub/ag-videosimages/metadata-profiles-fdos/-/blob/master/MareHub_AGVI_iFDO.md
		"ifdo":{'utc':'image-datetime','lat':'image-latitude','lon':'image-longitude','dep':'image-depth','hgt':'image-meters-above-ground'},

		# Definition of field/column names according to the "Acquisition, Curation and Management Workflow"
		# for marine image data https://www.nature.com/articles/sdata2018181
		"acmw":{'utc':'SUB_datetime','lat':'SUB_latitude','lon':'SUB_longitude','dep':'SUB_depth','hgt':'SUB_distance'},

		# Definition of field/colum names as they occur in a DSHIP export file

		# for RV Sonne posidonia beacons
		"SO_NAV-2_USBL_Posidonia":{1:{'utc':'date time','lat':'USBL.PTSAG.1.Latitude','lon':'USBL.PTSAG.1.Longitude','dep':'USBL.PTSAG.1.Depth'},
									2:{'utc':'date time','lat':'USBL.PTSAG.2.Latitude','lon':'USBL.PTSAG.2.Longitude','dep':'USBL.PTSAG.2.Depth'},
									4:{'utc':'date time','lat':'USBL.PTSAG.4.Latitude','lon':'USBL.PTSAG.4.Longitude','dep':'USBL.PTSAG.4.Depth'},
									5:{'utc':'date time','lat':'USBL.PTSAG.5.Latitude','lon':'USBL.PTSAG.5.Longitude','dep':'USBL.PTSAG.5.Depth'}
		},

		# for RV Sonne itself (GPS)
		"SO_NAV-1_GPS_Saab":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},


		# for RV Maria S Merian sonardyne beacons
		"MSM_NAV-2_USBL_Sonardyne":{2104:{'utc':'date time','lat':'Ranger2.PSONLLD.2104.position_latitude','lon':'Ranger2.PSONLLD.2104.position_longitude','dep':'Ranger2.PSONLLD.2104.depth'},
									2105:{'utc':'date time','lat':'Ranger2.PSONLLD.2105.position_latitude','lon':'Ranger2.PSONLLD.2105.position_longitude','dep':'Ranger2.PSONLLD.2105.depth'}
		},

		# for RV Maria S Metian itself (GPS)
		"MSM_NAV-1_GPS_Debeg4100":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},

		# Definition of field/column names according to the DSM Workbench
		"workbench": {},

		# Definition of field/column names required for assigning EXIF infos to a JPG file
		"exif":{'utc':'CreateDate','lat':'GPSLatitude','lon':'GPSLongitude','dep':'GPSAltitude','hgt':'GPSDestDistance'},

		# Definition of field/column names according to the AWI O2A GeoCSV standard
		# https://confluence.digitalearth-hgf.de/display/DM/O2A+GeoCSV+Format
		# Warning: GeoCSVs need an additional WKT column: geometry [point] with values like: POINT(latitude longitude)
		# Warning: depth and altitude are guessed as i could not find it in the documentation
		"o2a":{'utc':'datetime','lat':'latitude [deg]','lon':'longitude [deg]','dep':'depth [m]','hgt':'altitude [m]'},

		# Definition of field/column names according to the OFOP software
		# Warning: OFOP requires two separate columns for date and time
		# Warning: Depth can also be in column SUB1_USBL_Depth
		# ---- USBL depth kommt vom USBL System, nur depth von einem (online/logging) Drucksensor, manchmal gibt es nur USBL.
		# Warning: It does not have to be SUB1 it can also be SUB2, SUB3, ...
		"ofop":{'utc':'Date\tTime','lat':'SUB1_Lat','lon':'SUB1_Lon','dep':'SUB1_Depth','hgt':'SUB1_Altitude'},

		# Definition of field/column names according to the world data center PANGAEA
		"pangaea":{
				'utc':'DATE/TIME',								# (1599)
				'lat':'LATITUDE',								# (1600)
				'lon':'LONGITUDE',								# (1601)
				'dep':'DEPTH, water [m]',						# (1619)
				'hgt':'Height above sea floor/altitude [m]'		# (27313)
				},

		# Definition of field/column names according to the annotation software BIIGLE
		"biigle":{'utc':'taken_at','lat':'lat','lon':'lng','dep':'gps_altitude','hgt':'distance_to_ground'}

}

att_header = {
	"mariqt":{
			'yaw':'yaw',		# in degrees
			'pitch':'pitch',	# in degrees
			'roll':'roll',		# in degrees
		},
}

navigation_equipment = {
	'SO':{'satellite':'SO_NAV-1_GPS_Saab','underwater':'SO_NAV-2_USBL_Posidonia'},
	'MSM':{'satellite':'','underwater':''}
}

date_formats = {"pangaea":"%Y-%m-%dT%H:%M:%S",
				"mariqt":"%Y-%m-%d %H:%M:%S.%f",
				"mariqt_files":"%Y%m%d_%H%M%S",
				"mariqt_short":"%Y-%m-%d %H:%M:%S",
				"gx_track":"%Y-%m-%dT%H:%M:%SZ",
				"dship":"%Y/%m/%d %H:%M:%S",
				"underway":"%Y-%m-%dT%H:%M:%S.%fZ"}

col_header = {	'pangaea':{'annotation_label':'Annotation label'},
				'mariqt':{	'uuid':'image-uuid',
							'img':'image-filename',
							'utc':'image-datetime',
							'lat':'image-latitude',
							'lon':'image-longitude',
							'dep':'image-depth',
							'hgt':'image-meters-above-ground',
							'alt':'image-altitude',
							'hash':'image-hash-sha256',
							'acqui':'image-acquisition-settings',
							'uncert':'image-coordinate-uncertainty-meters',
							'yaw':'image-camera-yaw-degrees',
							'pitch':'image-camera-pitch-degrees',
							'roll':'image-camera-roll-degrees',
							'pose':'image-camera-pose'
							},
				'exif':{	'img':'SourceFile',
							'uuid':'imageuniqueid'}
}

photo_types = ['jpg','png','bmp','raw','jpeg','tif']
video_types = ['mp4','mov','avi','mts','mkv','wmv']
image_types = photo_types + video_types

equipment_types = ['CAM','HYA','ENV','NAV','SAM','PFM']

colors = ['#94B242','#24589B','#DCB734','#E7753B','#A0BAAC','#CAD9A0','#82C9EB','#E9DCA6','#ED9A72','#D0DDD6','#EFF5E4','#E6F5FB','#F7F1DC','#F9DED2','#E8EEEB']
color_names = {'entity':'#94B242','process':'#24589B','infrastructure':'#DCB734','missing':'#ED9A72','error':'#E7753B','green':'#94B242','light_green':'#EFF5E4','blue':'#24589B','light_blue':'#E6F5FB','yellow':'#DCB734','light_yellow':'#F7F1DC','red':'#E7753B','light_red':'#F9DED2','grey':'#A0BAAC','light_grey':'#E8EEEB','mid_green':'#CAD9A0','mid_blue':'#82C9EB','mid_yellow':'#E9DCA6','mid_red':'#ED9A72','mid_grey':'#D0DDD6','dark_grey':'#6D7F77',}



############# iFDO ###########################################

iFOD_version = "v1.1.0"

class dataTypes(Enum): # default is string
	float = 0
	dict = 1
	text = 2 # just for gui elements to show bigger text field
	list = 3 # TODO needs to be handled
	uuid = 4
	int = 5

image_set_header_key = 'image-set-header'
image_set_items_key =  'image-set-items'

req_person_fields = ['name','email','orcid']

ifdo_mutually_exclusive_fields = [['image-depth','image-altitude']]

ifdo_header_core_fields = {
	'image-set-name':{'comment': 'A unique name for the image set, should include `<project>, <event>, <sensor>` and purpose'},
	'image-set-uuid':{'comment': 'A UUID (**version 4 - random**) for the entire image set', 'dataType': dataTypes.uuid},
	'image-set-handle':{'comment': 'A Handle URL (using the UUID?) to point to the landing page of the data set'},
	'image-set-ifdo-version':{'comment': 'The semantic version information of the iFDO standard used. The default is v1.0.0'},
}

keyValidPlusCustom = "$OTHER" # add this key to valid list if also custom values are allowed

ifdo_item_core_fields = {
	'image-datetime':{'comment': 'The fully-qualified ISO8601 UTC time of image acquisition (or start time of a video). E.g.: %Y-%m-%d %H:%M:%S.%f (in Python). You *may* specify a different date format using the optional iFDO capture field `image-datetime-format`'},
	'image-latitude':{'comment': 'Y-coordinate of the camera center in decimal degrees: D.DDDDDDD (use at least seven significant digits that is ca. 1cm resolution)', 'dataType': dataTypes.float},
	'image-longitude':{'comment': 'X-coordinate of the camera center in decimal degrees: D.DDDDDDD (use at least seven significant digits that is ca. 1cm resolution)', 'dataType': dataTypes.float},
	'image-depth':{'comment': 'Z-coordinate of camera center in meters. *Use this when camera is below water, then it has positive values.*', 'dataType': dataTypes.float, 'alt-fields': ['image-altitude']},
	'image-altitude':{'comment': 'Z-coordinate of camera center in meters. *Use this when camera is above water, then it has positive values.* You can also use image-depth with negative values instead!', 'dataType': dataTypes.float, 'alt-fields': ['image-depth']},
	'image-coordinate-reference-system':{'comment': 'The coordinate reference system, e.g. **EPSG:4326**'},
	'image-coordinate-uncertainty-meters':{'comment': 'The average/static uncertainty of coordinates in this dataset, given in meters. Computed e.g. as the standard deviation of coordinate corrections during smoothing / splining.', 'dataType': dataTypes.float},
	'image-context':{'comment': 'The high-level "umbrella" project'},
	'image-project':{'comment': 'The lower-level / specific expedition or cruise or experiment or ...'},
	'image-event':{'comment': 'One event of a project or expedition or cruise or experiment or ...'},
	'image-platform':{'comment': 'Platform URN or Equipment Git ID or Handle URL'},
	'image-sensor':{'comment': 'Sensor URN or Equipment Git ID or Handle URL'},
	'image-uuid':{'comment': 'UUID (**version 4 - random**) for the image file (still or moving)', 'dataType': dataTypes.uuid},
	'image-hash-sha256':{'comment': 'An SHA256 hash to represent the whole file (including UUID in metadata!) to verify integrity on disk'},
	'image-pi':{'comment': 'Information to identify the principal investigator. See details below', 'dataType': dataTypes.dict,
			'subFields':{
					'name':{'comment': 'Full name of principal investigator'},
					'orcid':{'comment': 'ORCID of principal investigator'},},},
	'image-creators':{'comment': 'A list containing dicts for all creators containing: {orcid:..., name:...}', 'dataType': dataTypes.list},
	'image-license':{'comment': 'License to use the data (should be FAIR, e.g. **CC-BY** or CC-0)'},
	'image-copyright':{'comment': 'Copyright sentence / contact person or office', 'dataType': dataTypes.text},
	'image-abstract':{'comment': '500 - 2000 characters describing what, when, where, why and how the data was collected. Includes general information on the event (aka station, experiment), e.g. overlap between images/frames, parameters on platform movement, aims, purpose of image capture etc. You can use \'___field-name___\' to insert field values', 'dataType': dataTypes.text},
}

ifdo_content_fields = {
	'image-entropy':{'comment': 'Information content of an image / frame according to Shannon entropy.', 'dataType': dataTypes.float},
	'image-particle-count':{'comment': 'Counts of single particles/objects in an image / frame', 'dataType': dataTypes.int},
	'image-average-color':{'comment': 'The average colour for each image / frame and the `n` channels of an image (e.g. 3 for RGB)\nFormat: [int,int,int]'},
	'image-mpeg7-colorlayout':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-colorstatistic':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-colorstructure':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-dominantcolor':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-edgehistogram':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-homogeneoustexture':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-mpeg7-scalablecolor':{'comment': 'An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings.\nFormat: [float,float,...]'},
	'image-annotation-labels':{'comment': 'All the labels used in the image-annotations. Specified by an id (e.g. AphiaID), a human-readable name and an optional description.\nFormat: [{id:`<LID>`,name:string,info:`<description>`},...]'},
	'image-annotation-creators':{'comment': "All the annotators that created image-annotations. Specified by an id (e.g. ORCID), a human-readable name and an optional type specifying the annotator's expertise.\nFormat: [{id:`<ORCID/UUID>`,name:string,type:string (expert, non-expert, AI)},...]"},
	'image-annotations':{'comment': 'This field is mighty powerful! It stores all annotations as a list of dictionaries of 3-4 fields: shape, coordinates, labels and (optional) frames. See further explanations below. The list of labels specifies the IDs or names of objects and annotators and their confidence. These should be specified in an `image-annotation-labels` and `image-annotation-creators` field (see above) to provide more information on the values used in these fields.\nFormat: [{coordinates:...,labels:...,shape:,...,frames:...},`<ANNOTATION-2>`,...]',
			'subFields':{
					'shape':{'comment': 'The annotation shape is specified by a keyword (allowed values: see previous column).', 'valid': ['single-pixel', 'polyline', 'polygon', 'circle', 'rectangle', 'ellipse', 'whole-image']},
					'coordinates':{'comment': 'The pixel coordinates of one annotation. The top-left corner of an image is the (0,0) coordinate. The x-axis is the horizontal axis. Pixel coordinates may be fractional. Coordinates can be given as a list of lists in case of video annotations that change coordinates over time (see `image-annotation:frames` below). Otherwise it is just a list of floats. The required number of pixel coordinates is defined by the shape (0 for whole-image, 2 for single-pixel, 3 for circle, 8 for ellipse/rectangle, 4 or more for polyline, 8 or more for polygon). The third coordinate value of a circle defines the radius. The first and last coordinates of a polygon must be equal.\nFormat: [[p1.x,p1.y,p2x,p2.y,...]..]'},
					'labels':{'comment': 'A list of labels and annotators for one annotation. Use label IDs and annotator IDs here. The optional confidence in an annotation can be given as a float between 0 (100% uncertain) and 1 (100% certain). The confidence can be given independently for each label. Labels are independent of frames. The `created-at` field contains an ISO8601 string like `2011-10-05T14:48:00.000Z`\nFormat: [{label: `<LID>`, annotator: `<ORCID/UUID>`, created-at: `<datetime>`, confidence: `<float>`},...]'},
					'frames':{'comment': '(only required for video annotations) Frame times (in seconds from the beginning of a video) of a video annotation. Each frame time is linked to one entry in `image-annotations:coordinates` at the same position in the list, which specifies the current coordinates of the annotation at that frame.\nFormat: [f1,...]'},},},
}

ifdo_capture_fields = {
	'image-acquisition':{'comment': 'photo: still images, video: moving images, slide: microscopy images / slide scans', 'valid': ['photo', 'video', 'slide']},
	'image-quality':{'comment': "raw: straight from the sensor, processed: QA/QC'd, product: image data ready for interpretation", 'valid': ['raw', 'processed', 'product']},
	'image-deployment':{'comment': 'mapping: planned path execution along 2-3 spatial axes, stationary: fixed spatial position, survey: planned path execution along free path, exploration: unplanned path execution, experiment: observation of manipulated environment, sampling: ex-situ imaging of samples taken by other method', 'valid': ['mapping', 'stationary', 'survey', 'exploration', 'experiment', 'sampling']},
	'image-navigation':{'comment': 'satellite: GPS/Galileo etc., beacon: USBL etc., transponder: LBL etc., reconstructed: position estimated from other measures like cable length and course over ground', 'valid': ['satellite', 'beacon', 'transponder', 'reconstructed']},
	'image-scale-reference':{'comment': '3D camera: the imaging system provides scale directly, calibrated camera: image data and additional external data like object distance provide scale together, laser marker: scale information is embedded in the visual data, optical flow: scale is computed from the relative movement of the images and the camera navigation data', 'valid': ['3D camera', 'calibrated camera', 'laser marker', 'optical flow']},
	'image-illumination':{'comment': 'sunlight: the scene is only illuminated by the sun, artificial light: the scene is only illuminated by artificial light, mixed light: both sunlight and artificial light illuminate the scene', 'valid': ['sunlight', 'artificial light', 'mixed light']},
	'image-pixel-magnitude':{'comment': 'average size of one pixel of an image', 'valid': ['km', 'hm', 'dam', 'm', 'cm', 'mm', 'µm']},
	'image-marine-zone':{'comment': 'seafloor: images taken in/on/right above the seafloor, water column: images taken in the free water without the seafloor or the sea surface in sight, sea surface: images taken right below the sea surface, atmosphere: images taken outside of the water, laboratory: images taken ex-situ', 'valid': ['seafloor', 'water column', 'sea surface', 'atmosphere', 'laboratory']},
	'image-spectral-resolution':{'comment': 'grayscale: single channel imagery, rgb: three channel imagery, multi-spectral: 4-10 channel imagery, hyper-spectral: 10+ channel imagery', 'valid': ['grayscale', 'rgb', 'multi-spectral', 'hyper-spectral']},
	'image-capture-mode':{'comment': 'whether the time points of image capture were systematic, human-truggered or both', 'valid': ['timer', 'manual', 'mixed']},
	'image-fauna-attraction':{'comment': 'Allowed: none, baited, light', 'valid': ['none', 'baited', 'light']},
	'image-area-square-meter':{'comment': 'The footprint of the entire image in square meters', 'dataType': dataTypes.float},
	'image-meters-above-ground':{'comment': 'Distance of the camera to the seafloor in meters', 'dataType': dataTypes.float},
	'image-acquisition-settings':{'comment': 'All the information that is recorded by the camera in the EXIF, IPTC etc. As a dict. Includes ISO, aperture, etc.', 'dataType': dataTypes.dict},
	'image-camera-yaw-degrees':{'comment': "Camera view yaw angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation directions according to \'right-hand rule\'. I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward with top side towards north.", 'dataType': dataTypes.float},
	'image-camera-pitch-degrees':{'comment': "Camera view pitch angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation directions according to \'right-hand rule\'. I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward with top side towards north.", 'dataType': dataTypes.float},
	'image-camera-roll-degrees':{'comment': "Camera view roll angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation directions according to \'right-hand rule\'. I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward with top side towards north.", 'dataType': dataTypes.float},
	'image-overlap-fraction':{'comment': 'The average overlap of two consecutive images i and j as the area images in both of the images (A_i * A_j) divided by the total area images by the two images (A_i + A_j - A_i * A_j): f = A_i * A_j / (A_i + A_j - A_i * A_j) -> 0 if no overlap. 1 if complete overlap', 'dataType': dataTypes.float},
	'image-datetime-format':{'comment': 'A date time format string in Python notation (e.g. %Y-%m-%d %H:%M:%S.%f) to specify a different date format used throughout the iFDO file. The assumed default is the one in brackets. Make sure to reach second-accuracy with your date times!'},
	'image-camera-pose':{'comment': 'Information required to specify camera pose. For details on subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'pose-utm-zone':{'comment': 'The UTM zone number'},
					'pose-utm-epsg':{'comment': 'The EPSG code of the UTM zone'},
					'pose-utm-east-north-up-meters':{'comment': 'The position of the camera center in UTM coordinates.\nFormat: [float,float,float]'},
					'pose-absolute-orientation-utm-matrix':{'comment': '3x3 row-major float rotation matrix that transforms a direction in camera coordinates (x,y,z = right,down,line of sight) into a direction in UTM coordinates (x,y,z = easting,northing,up)}', 'dataType': dataTypes.list},},},
	'image-camera-housing-viewport':{'comment': 'Information on the camera pressure housing viewport (the glass). For details on subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'viewport-type':{'comment': 'e.g.: flatport, domeport, other'},
					'viewport-optical-density':{'comment': 'Unit-less optical density number (1.0=vacuum)', 'dataType': dataTypes.float},
					'viewport-thickness-millimeter':{'comment': 'Thickness of viewport in millimeters', 'dataType': dataTypes.float},
					'viewport-extra-description':{'comment': 'A textual description of the viewport used', 'dataType': dataTypes.text},},},
	'image-flatport-parameters':{'comment': 'Information required to specify the characteristics of a flatport camera housing. For details on subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'flatport-lens-port-distance-millimeter':{'comment': 'The distance between the front of the camera lens and the inner side of the housing viewport in millimeters.', 'dataType': dataTypes.float},
					'flatport-interface-normal-direction':{'comment': '3D direction vector to specify how the view direction of the lens intersects with the viewport (unit-less, (0,0,1) is "aligned")\nFormat: [float, float, float]'},
					'flatport-extra-description':{'comment': 'A textual description of the flatport used', 'dataType': dataTypes.text},},},
	'image-domeport-parameters':{'comment': 'Information required to specify the characteristics of a domeport camera housing. For details on subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'domeport-outer-radius-millimeter':{'comment': 'Outer radius of the domeport - the part that has contact with the water.', 'dataType': dataTypes.float},
					'domeport-decentering-offset-xyz-millimeter':{'comment': '3D offset vector of the camera center from the domeport center in millimeters\nFormat: [float,float,float]'},
					'domeport-extra-description':{'comment': 'A textual description of the domeport used', 'dataType': dataTypes.text},},},
	'image-camera-calibration-model':{'comment': 'Information required to specify the camera calibration model. For details on the subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'calibration-model-type':{'comment': 'e.g.: rectilinear air, rectilinear water, fisheye air, fisheye water, other'},
					'calibration-focal-length-xy-pixel':{'comment': '2D focal length in pixels\nFormat: [float, float]'},
					'calibration-principal-point-xy-pixel':{'comment': '2D principal point of the calibration in pixels (top left pixel center is 0,0, x right, y down)\nFormat: [float,float]'},
					'calibration-distortion-coefficients':{'comment': 'rectilinear: k1, k2, p1, p2, k3, k4, k5, k6, fisheye: k1, k2, k3, k4', 'dataType': dataTypes.list},
					'calibration-approximate-field-of-view-water-xy-degree':{'comment': 'Proxy for pixel to meter conversion, and as backup\nFormat: [float, float]'},
					'calibration-model-extra-description':{'comment': 'Explain model, or if lens parameters are in mm rather than in pixel', 'dataType': dataTypes.text},},},
	'image-photometric-calibration':{'comment': 'Information required to specify the photometric calibration. For details on the subfields see rows below.', 'dataType': dataTypes.dict,
			'subFields':{
					'photometric-sequence-white-balancing':{'comment': 'A text on how white-balancing was done.', 'dataType': dataTypes.text},
					'photometric-exposure-factor-RGB':{'comment': 'RGB factors applied to this image, product of ISO, exposure time, relative white balance\nFormat: [float, float, float]'},
					'photometric-sequence-illumination-type':{'comment': 'e.g. "constant artificial", "globally adapted artificial", "individually varying light sources", "sunlight", "mixed")'},
					'photometric-sequence-illumination-description':{'comment': 'A text on how the image sequence was illuminated', 'dataType': dataTypes.text},
					'photometric-illumination-factor-RGB':{'comment': 'RGB factors applied to artificial lights for this image\nFormat: [float, float, float]'},
					'photometric-water-properties-description':{'comment': 'A text describing the photometric properties of the water within which the images were capture', 'dataType': dataTypes.text},},},
	'image-objective':{'comment': 'A general translation of the aims and objectives of the study, as they pertain to biology and method scope. This should define the primary and secondary data to be measured and to what precision.', 'dataType': dataTypes.text},
	'image-target-environment':{'comment': 'A description, delineation, and definition of the habitat or environment of study, including boundaries of such', 'dataType': dataTypes.text},
	'image-target-timescale':{'comment': 'A description, delineation, and definition of the period, interval or temporal environment of the study.', 'dataType': dataTypes.text},
	'image-spatial-contraints':{'comment': 'A description / definition of the spatial extent of the study area (inside which the photographs were captured), including boundaries and reasons for constraints (e.g. scientific, practical)', 'dataType': dataTypes.text},
	'image-temporal-constraints':{'comment': 'A description / definition of the temporal extent, including boundaries and reasons for constraints (e.g. scientific, practical)', 'dataType': dataTypes.text},
	'image-time-synchronisation':{'comment': 'Synchronisation procedure and determined time offsets between camera recording values and UTC', 'dataType': dataTypes.text},
	'image-item-identification-scheme':{'comment': 'How the images file names are constructed. Should be like this `<project>_<event>_<sensor>_<date>_<time>.<ext>`', 'dataType': dataTypes.text},
	'image-curation-protocol':{'comment': 'A description of the image and metadata curation steps and results', 'dataType': dataTypes.text},
}

ifdo_coreFields = {**ifdo_header_core_fields, **ifdo_item_core_fields}
ifdo_fields =  {**ifdo_coreFields, **ifdo_content_fields, **ifdo_capture_fields}



# icons for iFDO creation wizard notebook to retrieve them centrally from pip package
myPath = os.path.dirname(__file__)
icon_check = open(myPath + "/for_notebooks/icons/checkbox-circle-line_green.png", "rb").read()
icon_checkDisabled = open(myPath + "/for_notebooks/icons/checkbox-circle-line_gray.png", "rb").read()
icon_error = open(myPath + "/for_notebooks/icons/error-warning-line_red.png", "rb").read()
icon_errorDisabled = open(myPath + "/for_notebooks/icons/error-warning-line_gray.png", "rb").read()
icon_warning = open(myPath + "/for_notebooks/icons/error-warning-line_orange.png", "rb").read()