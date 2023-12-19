

"""def make_catalogue(self):
    out_json = {}
    last_line = ""
    sample_ids = []
    with open(self.path + "/" + self.cat_name, "r") as idlist:
        lines = idlist.readlines()
        for line in lines:
            # finds all lines of type " id: "[word]""
            x = re.findall(r'[id: "]+[\w]*[-]*[\w]+["]', line)
            if x:
                # remove "id" with split and "" with strip
                out_json[x[0].split(" id: ")[1].strip('\"')] = {
                    "color": None,
                    "description": last_line.split("\n")[0]
                }
            last_line = line
    # try:
    #    with open(os.path.abspath(os.path.dirname(__file__)) + "/config/file_inst.json", "r") as of:
    #        inst_ids = json.load(of)["ids"]
    # except FileNotFoundError:
    #    raise FileNotFoundError("Could not load config/file_inst.json because file does not exists!")

    j_data = json.dumps(out_json, indent=4, sort_keys=True, separators=(",", ": "), ensure_ascii=False)
    with open(self.path + "sample_catalogue.json", "w+") as of:
        of.write(j_data)"""