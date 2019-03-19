import argparse
import sentinelhub
import numpy as np
from shapely.geometry import shape, Polygon, MultiPolygon, MultiLineString
import sys
from sentinelhub import BBoxSplitter, OsmSplitter, TileSplitter, read_data, CRS, DataSource, transform_bbox, BBox
from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox, CustomUrlParam


def main():
    args = parse_args()

    grid = args.grid.split(",")
    coords = [float(x.strip()) for x in args.coords.split(",")]

    # if args.geo_json_file:
    #     INPUT_FILE = args.data_file
    #
    #     geo_json = read_data(INPUT_FILE)

    area = Polygon([[coords[0], coords[1]], [coords[0], coords[3]], [coords[2], coords[3]], [coords[2], coords[1]]])
    bbox_splitter = BBoxSplitter([area], CRS.WGS84,
                                 (int(grid[0]), int(grid[1])), reduce_bbox_sizes=True)

    img_dict = make_request(bbox_splitter, args.instance_id, args.util, args.width, args.height, args.maxcc, args.time, args.start_time, args.end_time)

    if args.util == 'info':
        print_info(img_dict, args.maxcc, args.start_time, args.end_time)


def parse_args():
    parser = argparse.ArgumentParser(description="Download satellite images using SentinelHub API")
    parser.add_argument('--util',
                        help="Utility of CLI. This command can list information about imagery within the given constraints or download.",
                        choices=['info', 'download'],
                        required=False,
                        default='info')
    parser.add_argument('--coords',
                        help="CSV list of latitude & longitude coords. These are longitude and latitude coordinates of"
                             " upper left and lower right corners of area.",
                        required=True)
    parser.add_argument('--time', help="Time of image taken. Format is Datetime: 'xxxx-xx-xx'",
                        required='--start-time' not in sys.argv and '--end-time' not in sys.argv)
    parser.add_argument('--start-time', help="Start of Time frame. Format is Datetime: 'xxxx-xx-xx'",
                        required='--time' not in sys.argv and '--end-time' in sys.argv)
    parser.add_argument('--end-time', help="End of time frame. Format is Datetime: 'xxxx-xx-xx'",
                        required='--time' not in sys.argv and '--start-time' in sys.argv)
    parser.add_argument("--width", default=512,
                        help="Width of image")
    parser.add_argument("--height", default=512,
                        help="Height of image")
    parser.add_argument("--instance-id",
                        required=True,
                        help="Instance ID of configuration. This can be configured through the Sentinelhub Configuration Utility.")
    parser.add_argument("--maxcc",
                        default=1.0,
                        type=float,
                        help="Maximum cloud coverage for the area.")
    # parser.add_argument("--geo-json-file",
    #                     required=False,
    #                     help="Path to the data file containing geo coordinates.")
    parser.add_argument("--grid",
                        required=True,
                        help="The grid in which images will be split into. CSV list of two values e.g: 4,5 will be a 4x5 grid.")

    return parser.parse_args()


def print_info(img_dict, maxcc, start_time, end_time):
    total = 0
    for req, img in img_dict.items():
        if len(img) > 0:
            total += 1
            print('\nReturned data is of type = {} and length {}.'.format(type(img),
                                                                        len(img)))
            print('Single element in the list is of type {} and has shape {}'.format(type(img[-1]),
                                                                                     img[-1].shape))
            print('There are {} Sentinel-2 images available for the time and area specified.\n'.format(len(img)))
            print("Area: {}".format(req.bbox.__repr__()))
            print('These {} images were taken on the following dates:'.format(len(img)))
            for index, date in enumerate(req.get_dates()):
                print(' - image {} was taken on {}'.format(index, date))
        else:
            if not maxcc or maxcc == 1.0:
                print(
                    'No images exist for the specified area & time-frame: \nstart time: {} \nend time: {}'
                    '\nPlease specify a different time frame.'
                        .format(start_time, end_time))

            else:
                print(
                    'No images exist for the specified coords & time-frame: \nstart time: {} \nend time: {} '
                    '\nPlease specify a different time frame or set a different max cloud coverage.'
                        .format(start_time, end_time))
    print("\nTotal images: {}".format(total))


def make_request(bbox_splitter, instance_id, util, width, height, maxcc, time=None,  start_time=None, end_time=None):
    layer = 'TRUE-COLOR-S2-L1C'
    bbox_list = bbox_splitter.get_bbox_list()
    img_dict = {}
    for box in bbox_list:
        wms_true_color_request = WmsRequest(data_folder='data',
                                            layer=layer,
                                            bbox=box,
                                            time=(start_time, end_time) if not time == 'latest' else 'latest',
                                            width=int(width), height=int(height),
                                            maxcc=maxcc,
                                            instance_id=instance_id,
                                            custom_url_params={CustomUrlParam.TRANSPARENT: True})
        if util == 'download':
            wms_true_color_img = wms_true_color_request.get_data(save_data=True)
        elif util == 'info':
            wms_true_color_img = wms_true_color_request.get_data(save_data=False)
        img_dict[wms_true_color_request] = wms_true_color_img
    return img_dict


if __name__ == "__main__":
    main()
