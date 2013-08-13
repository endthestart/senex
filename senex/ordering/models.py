# from decimal import Decimal
#
# from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models
# from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

dimension_units = (('cm', 'cm'), ('mm', 'mm'), ('in', 'in'))

weight_units = (('kg', 'kg'), ('lb', 'lb'))


def default_dimension_unit():
    return 'mm'


def default_weight_unit():
    return 'lb'


# class CategoryManager(models.Manager):
#     def active(self, **kwargs):
#         return self.filter(is_active=True, **kwargs)
#
#     def by_site(self, site=None, **kwargs):
#         """Get all categories for this site"""
#         if not site:
#             site = Site.objects.get_current()
#
#         site = site.id
#
#         return self.active(site__id__exact = site, **kwargs)
#
#     def get_by_site(self, site=None, **kwargs):
#         if not site:
#             site = Site.objects.get_current()
#
#         return self.active().get(site=site, **kwargs)
#
#     def root_categories(self, site=None, **kwargs):
#         """Get all root categories."""
#
#         if not site:
#             site = Site.objects.get_current()
#
#         return self.active(parent__isnull=True, site=site, **kwargs)
#
#     def search_by_site(self, keyword, site=None, include_children=False):
#         """Search for categories by keyword.
#         Note, this does not return a queryset"""
#
#         if not site:
#             site = Site.objects.get_current()
#
#         cats = self.active().ilter(
#             Q(name__icontains=keyword) |
#             Q(meta__icontains=keyword) |
#             Q(description__icontains=keyword),
#             site=site
#         )
#
#         if include_children:
#             # get all the children in the categories found
#             cats = [cat.get_active_children(include_self=True) for cat in cats]
#
#         # sort properly
#         # if cats:
#         #     fastsort = [(c.ordering, c.name, c) for c in get_flat_list(cats)]
#         #     fastsort.sort()
#         #     # extract the cat list
#         #     cats = zip(*fastsort)[2]
#         return cats


class Category(models.Model):
    """
    Basic hierarchical category model for storing products
    """
    name = models.CharField(
        _("name"),
        max_lenght=200,
    )
    slug = models.SlugField(
        _("slug"),
        help_text=_("Used for URLs, auto-generated from name if blank"),
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
    )
    meta = models.TextField(
        _("meta description"),
        blank=True,
        null=True,
        help_text=_("Meta description for this category"),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        help_text=_("Description of the category."),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override alphabetical order in the category display."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        blank=True,
        help_text=_("Whether or not the category is active."),
    )
    related_categories = models.ManyToManyField(
        'self',
        blank=True,
        null=True,
        verbose_name=_('related categories'),
        related_name='related_categories',
    )
    #objects = CategoryManager()

    def _get_main_image(self):
        img = False
        return img

    main_image = property(_get_main_image)
#
#     def active_products(self, variations=False, include_children=False, **kwargs):
#         """Variations determines whether or not product variations are included.
#         In most templates we are not returning all variations
#         """
#
#
# class CurrencyField(models.DecimalField):
#     __metaclass__ = models.SubfieldBase
#
#     def to_python(self, value):
#         try:
#             return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
#         except AttributeError:
#             return None


# class ProductManager(models.Manager):
#     def active(self, variations=True, **kwargs):
#         if not variations:
#             kwargs['productvariation__parent__isnull'] = True
#         return self.filter(active=True, **kwargs)


class Product(models.Model):
    """
    Anything that can be ordered should inherit this.
    """
    name = models.CharField(
        _("name"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The name of the product."),
    )
    slug = models.SlugField(
        _("slug"),
        blank=True,
        help_text=_("Used for URLs, auto-generated from name if blank."),
        max_length=255,
    )
    created = models.DateTimeField(
        _("date created"),
        auto_now_add=True,
        help_text=_("The date and time the item was created."),
    )
    modified = models.DateTimeField(
        _("date modified"),
        auto_now=True,
        help_text=_("The date and time the item was modified."),
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        verbose_name=_("category"),
    )
    ordering = models.IntegerField(
        _("ordering"),
        default=0,
        help_text=_("Override default alphabetical ordering"),
    )
    price = models.DecimalField(
        _("price"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The cost of the item.")
    )
    stock = models.DecimalField(
        _("stock"),
        max_digits=18,
        decimal_places=6,
        default='0',
    )
    short_description = models.TextField(
        _("short description of the product."),
        max_length=200,
        default='',
        blank=True,
        help_text=_("This should be a 1 or 2 line description of the product."),
    )
    description = models.TextField(
        _("description"),
        null=True,
        blank=True,
        help_text=_("This should be a more lengthy description of the product."),
    )
    meta = models.TextField(
        _("meta description"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("The meta description of the product.")
    )
    active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Denotes if the product is available or not.")
    )

    # objects = ProductManager()

    def _get_main_category(self):
        """Return the first category for the product"""
        if self.category.count() > 0:
            return self.category.all()[0]
        else:
            return None

    main_category = property(_get_main_category)

    def _get_main_image(self):
        img = False
        if self.productimage_set.count() > 0:
            img = self.productimage_set.order_by('sort')[0]

        if not img:
            try:
                #img = ProductImage.objects.filter(product__isnull=True).order_by('sort')[0]
                img = None
            except IndexError:
                import sys
                print >>sys.stderr, 'Warning: default product image not found'

        return img

    main_image = property(_get_main_image)

    def _in_stock(self):
        return self.stock > 0
    is_in_stock = property(_in_stock)

    def _available(self):
        return True
    is_available = property(_available)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        ordering = ('site', 'ordering', 'name')
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def save(self, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name, instance=self)

        super(Product, self).save(**kwargs)


# class Frame(Product):
#
#     STYLE_CHOICES = (
#         ("650b", _("650b")),
#         ("26", _("26")),
#         ("29", _("29")),
#     )
#
#     TYPE_CHOICES = (
#         ("mountain", _("Mountain")),
#         ("road", _("Road")),
#         ("cx", _("Cyclocross")),
#     )
#     style = models.CharField(
#         _("style"),
#         max_length=20,
#         choices=STYLE_CHOICES,
#         help_text=_("The style of the bike, mainly wheel size."),
#     )
#     frame_type = models.CharField(
#         _("type"),
#         max_length=20,
#         choices=TYPE_CHOICES,
#         help_text=_("The type of frame, mainly mountain or road.")
#     )
#
#
# class Bicycle(Product):
#     frame = models.ForeignKey(
#         'Frame',
#         null=False,
#         blank=False,
#         help_text=_("The frame used as the base of the bike."),
#     )
#
#     wheelset = models.TextField()
#     fork = models.TextField()
#     headset = models.TextField()
#     stem = models.TextField()
#     handlebars = models.TextField()
#     groupset = models.TextField()
#     saddle = models.TextField()
#     seatpost = models.TextField()
#
#
# class Geometry(models.Model):
#     seat_tube_length = models.TextField()
#     seat_tube_angle = models.TextField()
#     head_tube_length = models.TextField()
#     head_tube_angle = models.TextField()
#     top_tube_effective_length = models.TextField()
#     top_tube_actual_length = models.TextField()
#     bottom_bracket_drop = models.TextField()
#     chain_stay_length = models.TextField()
#     stand_over_height = models.TextField()
#     front_center = models.TextField()
#
#
# class Order(models.Model):
#     something = models.TextField(),
#
#
# class OrderProduct(models.Model):
#     product = models.ForeignKey(
#         'Product',
#     )
#     order = models.ForeignKey(
#         'Order',
#     )
