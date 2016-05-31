#!flask/bin/python
from app import db,models
import sys, getopt

def main(argv):
	id = ''
	ip = ''
	ref = ''
	try:
		opts, args = getopt.getopt(argv,"hi:a:r:",["id=","ip=","ref="])
	except getopt.GetoptError:
		print 'peta al inicio'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--id"):
			id = arg
		elif opt in ("-a", "--ip"):
			ip = arg
		elif opt in ("-r","--ref"):
			ref = arg
	u = models.Server(profile_id=id, ip=ip, ref=ref)
	db.session.add(u)
	db.session.commit()	

if __name__ == "__main__":
   main(sys.argv[1:])
