class People(object):
  def __init__(self, info):
    self.name   = info[0]
    self.title  = info[1]
    self.email  = info[2]
    self.phone  = info[3]

  def __unicode__(self):
    return self.name

Dan = People(info = (
          'Dan Driscoll',
          'Founder',
          'dan@theanou.com',
          '212653827628',
        )
      )

Tom = People(info = (
          'Tom Counsell',
          'Technical Director',
          'tom@theanou.com',
          '212662750819',
        )
      )

Tifawt = People(info = (
          'Tifawt Belaid',
          'Community Supporter',
          'tifawt@theanou.com',
          '212613342325',
        )
      )

Brahim = People(info = (
          'Brahim El Mansouri',
          'Director',
          'brahim@theanou.com',
          '212673753163',
        )
      )

Rabha = People(info = (
          'Rabha Akkaouai',
          'Trainer',
          'tounfite.products@gmail.com',
          '212623045998',
        )
      )

Mustapha = People(info = (
          'Mustapha Chaouai',
          'Trainer',
          'oued.ifrane.nahda@gmail.com',
          '212637637569',
        )
      )

Kenza = People(info = (
          'Kenza Oulaghda',
          'Trainer',
          'kenzatithrite1@gmail.com',
          '0637637565',
        )
      )

everyones_emails = [Dan.email, Tifawt.email, Tom.email, Brahim.email, Rabha.email, Mustapha.email, Kenza.email]

#todo: remove this whole file and use admin account information
#todo: or use this file to define groups (trainers, translators, etc)
