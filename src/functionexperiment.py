def directions(dir):
    if dir==90 :
        return "E"
    elif dir==0:
        return "N"
    elif dir==270:
        return "W"
    elif dir==180:
        return "S"

    elif dir=="E":
        return 90
    elif dir=="N":
        return 0
    elif dir=="S":
        return 180
    elif dir=="W":
        return 270

def target_reached():
    if self.Xe == self.Xt and self.Ye == self.Yt:
        com.send_targetreached(self)
        self.finished = True 
