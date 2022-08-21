
class MetaPackage:
    instances = []

    def __init__(self, pkgname, pkgtype=None, pkgorg=None):
        self.instances.append(self) # adding the instance to colllective
        if len(str(pkgname).split(':')) == 2:
            if pkgtype == "maven":
                if pkgorg == None:
                    self._pkg_name = pkgname.split(':')[1]
                    self._orgId = pkgname.split(':')[0]
        else:
            self._pkg_name = pkgname
            self._orgId = pkgorg
        self._exists = None
        self._pkg_type = pkgtype
        self._score = None
        self._timestamp = None
        self._verCount = None
        #self._pkg_ver = pkgver TBA

    def __repr__(self):
        return self._pkg_name

    def __str__(self):
        return str(self._pkg_name)

    def listall(self):
        lister = []
        lister.append(self._pkg_name)
        lister.append(self._pkg_type)
        lister.append(self._exists)
        lister.append(self._orgId)
        lister.append(self._score)
        lister.append(self._verCount)
        lister.append(self._timestamp)
        return lister
    
    def get_instances():
        return MetaPackage.instances

    @property
    def pkg_name(self):
        return self._pkg_name

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, a):
        self._author = a

    @property
    def author_email(self):
        return self._author_email

    @author_email.setter
    def author_email(self, a):
        self._author_email = a

    @property
    def exists(self):
        return self._exists
    
    @exists.setter
    def exists(self, a):
        self._exists = a

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, a):
        self._publisher = a

    @property
    def publisher_email(self):
        return self._publisher_email

    @publisher.setter
    def publisher(self, a):
        self._publisher_email = a

    @property
    def maintainer(self):
        return self._maintainer

    @maintainer.setter
    def maintainer(self, a):
        self._maintainer = a

    @property
    def maintainer_email(self):
        return self._maintainer_email

    @maintainer_email.setter
    def maintainer_email(self, a):
        self._maintainer_email = a 
    
    @property
    def forkCount(self):
        return self._forkCount

    @forkCount.setter
    def forkCount(self, a):
        self._forkCount = a

    @property
    def subsCount(self):
        return self._subsCount

    @subsCount.setter
    def subsCount(self, a):
        self._subsCount = a

    @property
    def starCount(self):
        return self._starCount

    @starCount.setter
    def starCount(self, a):
        self._starCount = a

    @property
    def downloadCount(self):
        return self._downloadCount

    @downloadCount.setter
    def downloadCount(self, a):
        self._downloadCount = a

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, a):
        self._score = a
 
    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, a):
        self._dependencies = a

    @property
    def issueCount(self):
        return self._issueCount

    @issueCount.setter
    def issueCount(self, a):
        self._issueCount = a

    @property
    def contributorCount(self):
        return self._contributorCount

    @contributorCount.setter
    def contributorCount(self, a):
        self._contributorCount = a

    @property
    def orgId(self):
        return self._orgId

    @orgId.setter
    def orgId(self, a):
        self._orgId = a

    @property
    def verCount(self):
        return self._verCount

    @verCount.setter
    def verCount(self, a):
        self._verCount = a

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, a): #unix timestamp
        self._timestamp = a

# not-supported for now: hasTests, testsSize, privateRepo