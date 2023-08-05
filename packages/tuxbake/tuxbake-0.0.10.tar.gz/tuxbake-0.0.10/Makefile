check: black pylint

black:
	LC_ALL=C.UTF-8 LANG=C.UTF-8 black --check --diff tuxbake/ tests/

pylint:
	pylint --disable=all --enable=elif,exceptions,stdlib,imports,variables,string,string_constant,logging,newstyle,classes --disable=C0411,C0412,E0401,E0611,E0202,R0201,R0401,W --enable=R1707,R1714,R1715,R1716,W0235,W0404,W0611,W1401,W1402,W1403,W1505 tuxbake/

test:
	PYTHONPATH=. python3 -m pytest --log-cli-level=INFO --cov-report term-missing -v --cov tuxbake --cov-report html --cov-report term --junitxml=report.xml tests/unit/
