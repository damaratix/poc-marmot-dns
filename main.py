# http: 302
# http:  403
# dns
# nconnection 
import dns.resolver
import time

__FILE_MONITOR = 'to-monitor.txt'
res = dns.resolver.Resolver(configure=False)
res.nameservers = ['8.8.4.4']

class myFile:
    _dbfile = "database-default.log"
    
    def loadDB(self, dbfile=None): 
        if dbfile is not None: 
            self._dbfile = dbfile
        self.hnd = open( self._dbfile,'a+')
        self.data =  self.hnd.readlines()

    def search_last(self,  domain ):
        lastone = None
        for line in self.data: 
            if domain in line:
                lastone = line.strip() 
        return lastone 

    def store(self, domain, esito):      
        time_string = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
        self.hnd.write("%s|%s|%s\n" % (time_string, domain, esito)) 

    def close(self):
        self.hnd.close() 

    
def changes(domain, answers):
    last = db.search_last(domain)
    print( "looking for: " + domain, end =" " )
    if last : 
        # is it changed since last seen ? 
        buf= last.split("|")[2]
        if (buf != "%s" % answers[0] ) :
            print ("==> CHANGED", end=" ")
            print ("was: (%s)  now: (%s) " % (buf, answers[0] ) )
            db.store(domain, answers[0])
        else: 
            print ("==> unaltered since last seen: %s" % buf)
        return (True)
    else: 
        return (False)

    
if __name__ == "__main__":

    db = myFile()
    db.loadDB("database.log")
    with open(__FILE_MONITOR) as fp:
        domain = fp.readline().strip()
        cnt = 1
        while domain:
            cnt += 1
            try: 
                answers = dns.resolver.resolve(domain.strip(), 'a')
            except dns.resolver.NXDOMAIN:
                answers=[]
                answers.append('nxdomain') 
            except dns.resolver.NoAnswer:
                answers=[]
                answers.append('unknown') 
            except dns.exception.Timeout:
                answers=[]
                answers.append('timeout') 
            except dns.resolver.NoResolverConfiguration:
                answers=[]
                answers.append('your network error? Timeout') 
            except dns.resolver.NoResolverConfiguration:
                answers=[]
                answers.append('your network error? Resolver Configuration') 
            except dns.resolver.NoNameservers:
                answers=[]
                answers.append('your network error? All nameservers failed to answer.') 
     
            if not changes(domain, answers):
                # first time we see this domain
                print ("==> new (%s)" % answers[0])
                db.store(domain, answers[0])
           
            domain = fp.readline().strip()

db.close()
