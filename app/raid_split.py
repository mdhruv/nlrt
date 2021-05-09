from app import constants
import random
import itertools

class Split:
    raids = []
    split_id = 0
    is_valid = False
    mains = set()
    annotations = {}
    
    def __init__(self, split_id):
        self.split_id = split_id
        self.raids = []
        self.mains = set()
        self.annotations = {}
        self.annotations["info"] = []
        self.annotations["warning"] = []
        self.annotations["error"] = []
        self.balance_score = 0
        self.social_score = 0
        self.loot_score = 0
        self.total_score = 0
    
    def sort_raids(self):
        size_map = {}
        new_raid_list = []
        for raid in self.raids:
            size_map[raid.get_size()] = size_map.get(raid.get_size(), [])
            size_map[raid.get_size()].append(raid)
        sorted_raids_by_size = sorted(size_map.items(), key=lambda x: x[0])
        for size, raid_list in sorted_raids_by_size:
            random.shuffle(raid_list)
            new_raid_list += raid_list
        self.raids = new_raid_list
    
    def populate_raids(self, selected_raiders, num_splits=2):
        role_dict = {}
        self.raids = []
        self.mains = set()
        
        for raid_id in range(num_splits):
            self.raids.append(Raid(raid_id))
        
        for raider in selected_raiders:
            role_dict[raider.role] = role_dict.get(raider.role, [])
            role_dict[raider.role].append(raider)
            self.mains.add(raider.get_main())
    
        for role, raiders_for_role in role_dict.items():
            random.shuffle(raiders_for_role)
            for raider in raiders_for_role:
                self.sort_raids()
                is_added = False
                for raid in self.raids:
                    if not is_added and raider.get_main() not in raid.mains_set:
                        raid.add_raider(raider)
                        is_added = True
                if not is_added:
                    self.annotations["error"].append("Error adding raider %s to split, already in every raid" % raider)  
    
    def validate(self, req_dict):
        for raid in self.raids:
            if not raid.validate(req_dict):
                self.is_valid = False
                self.annotations["error"].append("Raid %s is invalid." % raid.raid_id)
                return False
        self.is_valid = True
        return True

    def calculate_balance_score(self):
        total_score = 0
        for raid1, raid2 in itertools.combinations(self.raids, 2):
            total_score += 2 * (raid1.get_size() - raid2.get_size())**2
            for role in constants.Roles:
                total_score += (raid1.counts.get(role, 0) - raid2.counts.get(role, 0))**2
            for game_class in constants.Classes:
                total_score += abs(raid1.counts.get(game_class, 0) - raid2.counts.get(game_class, 0))
        return total_score
            
    def calculate_social_score(self):
        partner_count = 0
        friend_count = 0
        for main in self.mains:
            for raid1 in self.raids:
                for raid2 in self.raids:
                    if raid1 == raid2 or main not in raid1.raiders:
                        continue
                    if main.partner and main.partner.get_main() not in raid1.mains_set and main.partner.get_main() in raid2.mains_set:
                        self.annotations["warning"].append("Partners %s and %s in different raids!"%( main.name, main.partner.get_main().name))
                        partner_count += 1
                    
                    for friend in main.friends:
                        if friend.get_main() not in raid1.mains_set and friend.get_main() in raid2.mains_set:
                            self.annotations["warning"].append("Friends %s and %s in different raids!"%( main.name, friend.get_main().name))
                            friend_count += 1
        return 12 * partner_count + friend_count
    
    def calculate_loot_score(self, loot_dict):
        loot_score = 0
        for loot, raiders in loot_dict.items():
            for raider1, raider2 in itertools.combinations(raiders, 2):
                for raid in self.raids:
                    if raider1 in raid.raiders and raider2 in raid.raiders:
                        loot_score+=1
                        self.annotations["warning"].append("%s and %s both in the same raid for %s" % (raider1.name, raider2.name, loot))                   
        return loot_score
    
    def score(self, loot_dict):
        self.balance_score = self.calculate_balance_score()
        self.social_score = self.calculate_social_score()
        self.loot_score = self.calculate_loot_score(loot_dict)
        self.total_score = self.balance_score + self.social_score + self.loot_score
        return self.total_score
    
    def normalize(self, balance_norm, social_norm, loot_norm):
        self.balance_score = 1 - self.balance_score / balance_norm
        self.social_score = 1 - self.social_score / social_norm
        self.loot_score =  1 - self.loot_score / loot_norm
        self.total_score = (self.balance_score + self.social_score + self.loot_score) / 3
        self.annotations["info"].append("Total Score: %.4f" % self.total_score)
        self.annotations["info"].append("Balance Score: %.4f" % self.balance_score)
        self.annotations["info"].append("Social Score: %.4f" % self.social_score)
        self.annotations["info"].append("Loot Score : %.4f" % self.loot_score)
        return self.total_score
                         
    
    def table_format(self):
        raid_num = 1
        table = []
        title = []
        for raid in self.raids:
            raid.raiders = sorted(raid.raiders, key=lambda x:x.sort_key(), reverse=True)
            title.append("Raid %s" % raid_num)
            raid_num+=1
        title.append("Warnings")
        title.append("Info")
        table.append(title)
        
        index = 0
        while True:
            data_added = False
            data = []
            for raid in self.raids:
                if len(raid.raiders) > index:
                    data.append(raid.raiders[index].name)
                    data_added = True
                else:
                    data.append("")
            if len(self.annotations["warning"]) > index:
                data.append(self.annotations["warning"][index])
                data_added = True
            else:
                data.append("")
            if len(self.annotations["info"]) > index:
                data.append(self.annotations["info"][index])
                data_added = True
            else:
                data.append("")
            
            if data_added:
                table.append(data)
            else:
                return table
            index+=1
                                        
    def __repr__(self):
        raid_str = ""
        for raid in self.raids:
            raid_str += "\n%s" % raid
        return 'Split(%s) %s\nIs Valid: %s\nBalance Score: %s\nSocial Score: %s\nLoot Score: %s\nTotal Score: %s' % (self.split_id, raid_str, self.is_valid, self.balance_score, self.social_score, self.loot_score, self.total_score)
   

class Raid:
    raid_id = 0
    is_valid = False

    def __init__(self, raid_id):
        self.raid_id = raid_id
        self.raiders = []
        self.mains_set = set()
        self.counts = {}
    
    def add_raider(self, raider):
        self.raiders.append(raider)
        self.mains_set.add(raider.get_main())
        self.counts["Total"] = self.counts.get("Total", 0) + 1
        self.counts[raider.role] = self.counts.get(raider.role, 0) + 1
        self.counts[raider.game_class] = self.counts.get(raider.game_class, 0) + 1
        
        if raider.profession1:
            self.counts[raider.profession1] = self.counts.get(raider.profession1, 0) + 1
        if raider.profession2:
            self.counts[raider.profession2] = self.counts.get(raider.profession2, 0) + 1
        
        if raider.has_cooking:
            self.counts["Cooking"] = self.counts.get("Cooking", 0) + 1
        if raider.has_first_aid:
            self.counts["First Aid"] = self.counts.get("First Aid", 0) + 1
        if raider.has_fishing:
            self.counts["Fishing"] = self.counts.get("Fishing", 0) + 1
        if raider.is_raid_leader:
            self.counts["Raid Leader"] = self.counts.get("Raid Leader", 0) + 1

    def get_size(self):
        return len(self.raiders)
    
    def validate(self, req_dict):
        for req, num in req_dict.items():
            if self.counts.get(req, 0) < num:
                self.is_valid = False
                return False
        self.is_valid = True
        return True
            
    def __repr__(self):
        raiders_str = ", ".join(list(map(lambda x:x.name, self.raiders)))
        return '<Raid(%s) %s>' % (self.raid_id, raiders_str)

    

def _parse_req_string(req_string):
    requirement_dict = {}
    for req_string_split in req_string.split(";"):
        req_split = req_string_split.split(":")
        if len(req_split) != 2:
            print("Split not length 2  %s" % req_split)
            return None
        req, num = req_split
        if req not in constants.ParseMap:
            print("%s not in ParseMap" % req)
            return None
        if int(num) < 1 or int(num) > 25:
            return None
        requirement_dict[constants.ParseMap[req]] = int(num)
    return requirement_dict

def _parse_loot_string(loot_string, selected_raiders):
    loot_dict = {}
    raider_name_dict = dict(map(lambda x: (x.name.lower(), x), selected_raiders))
    for loot_string_split in loot_string.split(";"):
        loot_string_split_tuple = loot_string_split.split(":")
        if len(loot_string_split_tuple) != 2:
            print("Split not length 2  %s" % loot_string_split_tuple)
            return None
        loot, raider_list_str = loot_string_split_tuple
        raiders = set()
        for raider_str in raider_list_str.split(","):
            if raider_str.lower().strip() in raider_name_dict:
                raiders.add(raider_name_dict[raider_str.lower().strip()])
        if len(raiders) > 1:
            loot_dict[loot] = raiders
    return loot_dict
            
def CalculateSplits(selected_raiders, req_string, loot_string, num_splits, num_sims):
    req_dict = _parse_req_string(req_string)
    loot_dict = _parse_loot_string(loot_string, selected_raiders)
    if req_dict == None or loot_dict == None:
        return None
    valid_splits = []
    balance_norm = 0
    social_norm = 0
    loot_norm = 0
    for i in range(num_sims):
        split = Split(i)
        split.populate_raids(selected_raiders, num_splits=num_splits)
        split.validate(req_dict)
        if split.is_valid:
            split.score(loot_dict)
            valid_splits.append(split)
            balance_norm += split.balance_score
            social_norm += split.social_score
            loot_norm += split.loot_score
    
    for split in valid_splits:
        split.normalize(balance_norm, social_norm, loot_norm)
    
    sorted_splits = sorted(valid_splits, key=lambda x:x.total_score, reverse=True)
    return sorted_splits[:10]

    