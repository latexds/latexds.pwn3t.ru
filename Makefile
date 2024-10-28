all: www/privacy.html www/tos.html

www/privacy.html www/tos.html: www

www/privacy.html: root/privacy.html
	cpp -P $< > $@

www/tos.html: root/tos.html
	cpp -P $< > $@

www:
	mkdir -p $@
