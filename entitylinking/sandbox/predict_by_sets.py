def create_sets(fname):
	sets = {}
	curr_fb_id = ''
	curr_entity = ''
	curr_fb_label = ''
	with open(fname, encoding="utf-8") as f:
		header = f.readline()
		for line in f:
			if "ES-Response-For-Entry: " in line:
				curr_entity = line.split(' ')[1].strip('\n')
				sets[curr_entity] = {}
			elif "fbase:" in line:
				curr_fb_id = line.split(':')[1]
				curr_fb_label = line.split(':')[2].strip('\n')
				sets[curr_entity][curr_fb_id, curr_fb_label] = set()
			else:
				sets[curr_entity][curr_fb_id, curr_fb_label].add(line)
	return sets

def calc_links(sets):
	links = {}
	with open("final.txt", "w", encoding="utf-8") as of:
		for entry, value in sets.items():
			links[entry] = ''
			max_intersection = 0
			for fbid_label, set_data in value.items():
				for key, other_sets in sets.items():
					if key != entry:
						for some_id_label, s in other_sets.items():
							if len(set_data.intersection(s)) > max_intersection:
								max_intersection = len(set.intersection(s))
								links[entry] = fbid_label
			if links[entry]:
				of.write(entry + ':' + links[entry][0] + ':' + links[entry][1] + '\n')
	return links

print(calc_links(create_sets("values_one_page.txt")))