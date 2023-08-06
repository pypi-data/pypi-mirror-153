import threading

class ProcessLog:
    pass

class TrainLog:
    lock = threading.Lock()
    
    def getInputValue(value):
        val = "{}".format(value[0])
        for i in range(1,len(value)):
            val += ",{}".format(value[i])
        rtn = val + "\n"
        return rtn
    
    def add(self,path,logrow):
        self.lock.acquire()
        try:
            fs = open(path,"a+")
            
            fs.write(TrainLog.getInputValue(logrow))
            fs.close()
        except Exception as err:
            print(err)
        finally:
            self.lock.release()
        pass
    
    def get(self,path,points = 300):
        self.lock.acquire()
        rtn = []
        
        try:
            fs = open(path,"r")
            
            rs = fs.readlines()
            period = len(rs)//points
            for ri in range(len(rs)):
                if(ri%period != 0):
                    continue
                r = rs[ri]
                r = r[:-1]
                cs = r.split(',')
                
                for ci in range(len(cs)):
                    
                    if len(rtn) == ci:
                        rtn.append([])
                    len(rtn[ci])
                    rtn[ci].append(cs[ci])
            
            fs.close()
        except Exception as err:
            print(err)
        finally:
            self.lock.release()
        return rtn
    pass

tlog = TrainLog()

if __name__ == "__main__":
    
    pass