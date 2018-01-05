#coding:utf-8
from django.db import models

class Author(models.Model):
    """作者模型"""
    name = models.CharField(max_length=20)
    email = models.EmailField()
    descript = models.TextField()

    def __unicode__(self):
        return u'%s' % (self.name)

class Tag(models.Model):
    """博客分类"""
    tag_name=models.CharField(max_length=20)
    create_time=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name

class BlogManager(models.Manager):
    """docstring for BlogManager"""
    def title_count(self, keyword):
        return self.filter(caption__icontains=keyword).count()

    def tag_count(self, keyword):
        return self.filter(tags__icontains=keyword).count()

    def author_count(self, keyword):
        return self.filter(author__icontains=keyword).count()


class Blog(models.Model):
    """博客"""
    caption = models.CharField(max_length=50)
    author = models.ForeignKey(Author)  #一对一外键，关联作者模型
    tags = models.ManyToManyField(Tag, blank=True) #多对多字段，绑定下面的Tag模型
    content = models.TextField()  #Text长文本字段，可以写很多内容

    publish_time = models.DateTimeField(auto_now_add=True) #日期，新增自动写入
    update_time = models.DateTimeField(auto_now=True) #日期，修改自动更新
    recommend = models.BooleanField(default=False) #布尔字段，我用于标记是否是推荐博文
    read_num = models.IntegerField(default=0)   #阅读次数
    objects = models.Manager()
    count_objects = BlogManager()
    taglist = []

    def save(self, *args, **kwargs):
        super(Blog, self).save()
        for i in self.taglist:
            p, created = Tag.objects.get_or_create(tag_name=i)
            self.tags.add(p)

    def __unicode__(self):
        return u'%s %s %s' % (self.caption, self.author, self.publish_time)

    class Meta:
        #排序
        ordering=['-publish_time']


class Weibo(models.Model):
    massage = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.massage
