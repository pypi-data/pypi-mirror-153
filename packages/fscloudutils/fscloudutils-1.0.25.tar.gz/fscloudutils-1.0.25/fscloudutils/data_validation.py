import os
import json
from skimage import io
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

class OutputValidator:

    def __init__(self):
        pass

    def check_existence(self, required_files, localpath, plot_name):
        """
        checks for output files existence - does not check for output quality or validity
        :param required_files:
        :return:
        """

        def check(file_name):
            if not os.path.exists(file_name):
                temp = " output does not exists in dir."
                bad.append(file_name)
            elif os.stat(file_name).st_size <= 1:
                temp = " output is empty."
                empty.append(file_name)
            else:
                temp = " output exists in dir."
                good.append(file_name)
            return temp

        print("Checking file existence:")
        bad, good, empty = [], [], []
        for name in required_files:
            print(name + check(os.path.join(localpath, plot_name + "_" + name)))
        results_exists = False
        for fi in os.listdir(localpath):
            if os.path.isdir(os.path.join(localpath, fi)):
                if fi == "Results":
                    results_exists = True
                    name_excel = os.path.join(localpath, fi, "Excel", f"Analysis for {plot_name}.xlsx")
                    name_yield = os.path.join(localpath, fi, "Yield", f"{plot_name}_heatmap_side_both_Yield.png")
                    name_size = os.path.join(localpath, fi, "Size", f"{plot_name}_heatmap_side_both_Size.png")
                    for file_name in [name_excel, name_size, name_yield]:
                        print("checking " + os.path.basename(file_name))
                        print(file_name + check(file_name))
                    continue
                else:
                    print("checking row" + fi)
                    for name in ["data.csv", "data_sliced.csv"]:
                        print(name + check(os.path.join(localpath, fi, name)))

        if not results_exists:
            print("'Results' folder does not exist")
        return bad, good, empty

    def check_validity(self):
        print("Checking file validity:")
        return

    def check_quality(self):
        print("Checking file quality:")
        return

    def get_summary(self, bad, good, empty):
        summary = "<br>" + str(len(bad)) + " file(s) are missing:<br>"
        for i, b in enumerate(bad):
            summary += str(i + 1) + ". " + b + "<br>"
        summary += "<br>" + str(len(empty)) + " file(s) are empty:<br>"
        for i, e in enumerate(empty):
            summary += str(i + 1) + ". " + e + "<br>"
        summary += "<br>" + str(len(good)) + " file(s) OK:<br>"
        for i, g in enumerate(good):
            summary += str(i + 1) + ". " + g + "<br>"
        print(summary)
        return summary

    def validate_output(self, localpath, plot_name, required_files):
        bad, good, empty = self.check_existence(required_files, localpath, plot_name)
        self.check_validity()
        self.check_quality()
        return self.get_summary(bad, good, empty)


class InputValidator:
    """
    Validator class for input validation
    1. Metadata json validation
    2. Images validation
    3. nav files validation
    4. polygon validation
    """

    def __init__(self, data, localpath, universal_model_input_requirement):
        """
        constructor function
        :param data:
        :param localpath:
        """
        print("Input validation, may take few minutes...")
        self.data = data
        self.localpath = localpath
        self.general_metadata = {}
        self.universal_metadata = {}
        self.images = {}
        self.navs = {}
        self.polygon = {}
        self.universal_model_input_requirement = universal_model_input_requirement

    def run_validation(self):
        """
        runs all the tests sequentially
        :return:
        """
        # running validations
        self.validate_metadata()
        self.validate_images()
        self.validate_nav()
        self.validate_polygon()
        self.check_errors()

    def validate_metadata(self):
        """
        metadata json test
        checking for empty fields or illegal string
        :return:
        """
        print("Analyzing metadata...")
        for key in self.data.keys():
            if self.data[key] is not None and self.data[key] != "":
                self.general_metadata[key] = "OK"
                if key in self.universal_model_input_requirement:
                    self.universal_metadata[key] = "OK"
            else:
                self.general_metadata[key] = "Failed"
                if key in self.universal_model_input_requirement:
                    self.universal_metadata[key] = "Failed"
        print(json.dumps(self.general_metadata, indent=4))

    def validate_images(self):
        """
        checking image completness
        merely opening the image with the io library
        :return:
        """
        print("Analyzing images...")
        for root, dir, files in os.walk(self.localpath):
            for file in files:
                if file.endswith('.png'):
                    path = os.path.join(root, file)
                    try:
                        image = io.imread(path)
                        self.images[file] = "OK"
                    except FileNotFoundError:
                        self.images[file] = "Bad image file"
        print(json.dumps(self.images, indent=4))

    def validate_nav(self):
        """
        checking nav files validity
        opens every nav file and searching for "GPGGA" or "GNGGA", then checks the existence of satellite data
        :return:
        """
        print("Analyzing nav files...")
        for root, dir, files in os.walk(self.localpath):
            for file in files:
                if file.endswith('.nav'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r') as f:
                            read_data = f.read()
                            read_data = read_data.split('$')
                            for i, point in enumerate(read_data):
                                if ('GPGGA' in point or 'GNGGA' in point) and len(point.split(',')) > 6:
                                    self.navs[file] = "OK"
                                    break
                                else:
                                    pass
                                if i >= len(read_data):
                                    self.navs[file] = "Bad nav file"
                                    break
                    except:
                        self.navs[file] = "Bad nav file"
        print(json.dumps(self.navs, indent=4))

    def validate_polygon(self):
        """
        validating the existance of a polygon within the metadata json
        :return:
        """
        print("Analyzing polygon...")
        try:
            if "plot coordinates" in self.data.keys() and self.data["plot coordinates"] is not None:
                self.polygon["polygon"] = "OK"
            else:
                self.polygon["polygon"] = "Bad polygon"
        except:
            self.polygon["polygon"] = "Bad polygon"
        print(json.dumps(self.polygon, indent=4))

    def check_ok(self, dict):
        ok = 0
        not_ok = 0
        for n in dict.keys():
            if dict[n] is "OK":
                ok += 1
            else:
                not_ok += 1
        return ok, not_ok

    def print_summery(self, data, title):
        ok, not_ok = self.check_ok(data)
        if ok + not_ok > 0:
            print("%s summary: %d/%d" % (title, ok, ok + not_ok))
            print("test rate is %d%% success" % int(ok * 100 / (ok + not_ok)))
            output_dump = [n for n in data if data[n] is not 'OK']
            if len(output_dump) > 0:
                print(json.dumps(output_dump, indent=4))
            print("..........................................................................")
            print("..........................................................................")
            print("..........................................................................")
        else:
            print("%s summary: \"universal model input requirement\" missing or empty")

    def check_errors(self):
        """

        :return:
        """
        # template = "%s summary: %d/%d"
        print("\nANALYSIS SUMMARY: ")
        print("..........................................................................")
        print("..........................................................................")
        print("..........................................................................")
        self.print_summery(self.general_metadata, "METADATA JSON")
        self.print_summery(self.universal_metadata, "UNIVERSAL METADATA JSON")
        self.print_summery(self.images, "IMAGES")
        self.print_summery(self.navs, "NAV")
        self.print_summery(self.polygon, "POLYGON")


if __name__ == '__main__':
    localpath = "/home/yotam/PycharmProjects/FruitSpec_Amazon_System_V2/Hippocampus/input/HAREYG/140621/HRGJUN21/RNFCS170"
    data_path = "/home/yotam/PycharmProjects/FruitSpec_Amazon_System_V2/Hippocampus/input/HAREYG/140621/HRGJUN21/RNFCS170/RNFCS170_Metadata.json"
    data = json.load(open(data_path))
    input_validator = InputValidator(data, localpath)
    input_validator.run_validation()
