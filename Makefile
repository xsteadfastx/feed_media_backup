.PHONY: init clean docker-build publish

init:
	pipenv --three
	pipenv install --dev

clean:
	rm -rf *.pyc
	rm -rf .cache
	rm -rf .mypy_cache
	rm -rf .tox
	rm -rf __pycache__
	rm -rf build

docker-build: clean
	docker build -t feed_media_backup .

publish: clean
	pipenv run python setup.py publish
