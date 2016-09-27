all: tech.dot

tech.dot: json/technologies.json
	python tech.py $<

json/%.json: scraped/%.html
	@mkdir -p $(@D)
	python parse.py $< > $@
