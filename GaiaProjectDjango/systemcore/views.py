from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import  SystemCoreColourCode


class HomeView(TemplateView):
    template_name = 'systemcore/index.html'

class ColorCodeListView(ListView):
    model = SystemCoreColourCode  # Replace with your model name
    paginate_by = 15 # Optional: number of items per page
    ordering = ['name']  # Optional: default ordering of the list
    # Optional: customize the template and context variable 
    template_name = 'systemcore/colorcode_list.html'  # Replace with your template name
    context_object_name = 'objects'        # Optional: customize context variable

class ColorCodeDetailView(DetailView):
    model = SystemCoreColourCode  # Replace with your model name
    template_name = 'systemcore/colorcode_detail.html'  # Replace with your template name
    context_object_name = 'object'  # Optional: customize context variable

class ColorCodeCreateView(CreateView):
    model = SystemCoreColourCode  # Replace with your model name
    template_name = 'systemcore/colorcode_form.html'  # Replace with your template name
    fields = ['name', 'rgb_value', 'hex_code']  # Fields to include in the form
    success_url = reverse_lazy('systemcore:colorcode_list')  # Redirect after successful creation

class ColorCodeUpdateView(UpdateView):
    model = SystemCoreColourCode  # Replace with your model name
    template_name = 'systemcore/colorcode_form.html'  # Replace with your template name
    fields = ['name', 'rgb_value', 'hex_code']  # Fields to include in the form
    success_url = reverse_lazy('systemcore:colorcode_list')  # Redirect after successful update

class ColorCodeDeleteView(DeleteView):
    model = SystemCoreColourCode  # Replace with your model name
    template_name = 'systemcore/colorcode_confirm_delete.html'  # Replace with your template name
    success_url = reverse_lazy('systemcore:colorcode_list')  # Redirect after successful deletion
    context_object_name = 'object'  # Optional: customize context variable
def index(request):
    """
    View function for the home page of the site.
    This view renders the index.html template and can be used to display
    any initial data or context needed for the homepage.
    """
    return render(request, 'systemcore/index.html', {})
def about(request):
    """
    View function for the about page of the site.
    This view renders the about.html template and can be used to display
    information about the site, its purpose, or any other relevant details.
    """
    return render(request, 'systemcore/about.html', {})
def contact(request):
    """
    View function for the contact page of the site.
    This view renders the contact.html template and can be used to display
    contact information, a contact form, or any other relevant details for users
    to get in touch with the site administrators.
    """
    return render(request, 'systemcore/contact.html', {})
def help(request):
    """
    View function for the help page of the site.
    This view renders the help.html template and can be used to provide
    assistance, FAQs, or any other relevant information to help users navigate the site.
    """
    return render(request, 'systemcore/help.html', {})
def privacy_policy(request):
    """
    View function for the privacy policy page of the site.
    This view renders the privacy_policy.html template and can be used to display
    the site's privacy policy, detailing how user data is collected, used, and protected.
    """
    return render(request, 'systemcore/privacy_policy.html', {})
def terms_of_service(request):
    """
    View function for the terms of service page of the site.
    This view renders the terms_of_service.html template and can be used to display
    the site's terms of service, outlining the rules and guidelines for using the site.
    """
    return render(request, 'systemcore/terms_of_service.html', {})
def faq(request):
    """
    View function for the FAQ page of the site.
    This view renders the faq.html template and can be used to provide
    answers to frequently asked questions, helping users find quick solutions to common issues.
    """
    return render(request, 'systemcore/faq.html', {})
def sitemap(request):
    """
    View function for the sitemap page of the site.
    This view renders the sitemap.html template and can be used to display
    a structured list of the site's pages, helping users navigate the site more easily.
    """
    return render(request, 'systemcore/sitemap.html', {})
def terms_of_use(request):
    """
    View function for the terms of use page of the site.
    This view renders the terms_of_use.html template and can be used to display
    the site's terms of use, outlining the acceptable use policies and user responsibilities.
    """
    return render(request, 'systemcore/terms_of_use.html', {})
def cookie_policy(request):
    """
    View function for the cookie policy page of the site.
    This view renders the cookie_policy.html template and can be used to display
    the site's cookie policy, detailing how cookies are used, what data they collect,
    and how users can manage their cookie preferences.
    """
    return render(request, 'systemcore/cookie_policy.html', {})
def accessibility(request):
    """
    View function for the accessibility page of the site.
    This view renders the accessibility.html template and can be used to provide
    information about the site's accessibility features, guidelines, and resources
    to ensure that all users, including those with disabilities, can access and use the site effectively.
    """
    return render(request, 'systemcore/accessibility.html', {})
def legal_notice(request):
    """
    View function for the legal notice page of the site.
    This view renders the legal_notice.html template and can be used to display
    any legal disclaimers, notices, or information required by law regarding the site's operation,
    ownership, or content.
    """                             
    return render(request, 'systemcore/legal_notice.html', {})
def terms_of_sale(request):
    """
    View function for the terms of sale page of the site.
    This view renders the terms_of_sale.html template and can be used to display
    the site's terms of sale, outlining the conditions under which products or services are sold,
    including payment terms, delivery policies, and return/refund procedures.
    """
    return render(request, 'systemcore/terms_of_sale.html', {})
def copyright_notice(request):
    """
    View function for the copyright notice page of the site.
    This view renders the copyright_notice.html template and can be used to display
    the site's copyright information, including the copyright holder's name, the year of publication,
    and any relevant copyright statements or notices.
    """
    return render(request, 'systemcore/copyright_notice.html', {})
def data_protection(request):
    """
    View function for the data protection page of the site.
    This view renders the data_protection.html template and can be used to display
    information about how user data is collected, stored, and protected,
    including details on data security measures, user rights regarding their data,
    and how users can exercise those rights.
    """
    return render(request, 'systemcore/data_protection.html', {})
def user_agreement(request):
    """
    View function for the user agreement page of the site.
    This view renders the user_agreement.html template and can be used to display
    the site's user agreement, outlining the terms and conditions that users must agree to
    before using the site, including user responsibilities, rights, and any other relevant legal information.
    """
    return render(request, 'systemcore/user_agreement.html', {})
def community_guidelines(request):
    """
    View function for the community guidelines page of the site.
    This view renders the community_guidelines.html template and can be used to display
    the site's community guidelines, outlining the expected behavior of users within the community,
    including rules for interaction, content sharing, and any other relevant community standards.
    """
    return render(request, 'systemcore/community_guidelines.html', {})
def support(request):
    """
    View function for the support page of the site.
    This view renders the support.html template and can be used to provide
    information on how users can get help or support, including contact details,
    support hours, and links to support resources such as FAQs, forums, or help documentation.
    """
    return render(request, 'systemcore/support.html', {})
def feedback(request):
    """
    View function for the feedback page of the site.
    This view renders the feedback.html template and can be used to provide
    a form or instructions for users to submit feedback about the site,
    including suggestions, bug reports, or general comments.
    """
    return render(request, 'systemcore/feedback.html', {})
def resources(request):
    """
    View function for the resources page of the site.
    This view renders the resources.html template and can be used to provide
    links to additional resources, tools, or information that may be helpful to users,
    such as guides, tutorials, or external websites related to the site's content or purpose.
    """
    return render(request, 'systemcore/resources.html', {})
def news(request):
    """
    View function for the news page of the site.
    This view renders the news.html template and can be used to display
    the latest news, updates, or announcements related to the site or its content,
    including blog posts, articles, or any other relevant information that keeps users informed.
    """
    return render(request, 'systemcore/news.html', {})
def events(request):
    """
    View function for the events page of the site.
    This view renders the events.html template and can be used to display
    information about upcoming events, such as webinars, workshops, or community gatherings,
    including event details, dates, times, and registration information.
    """
    return render(request, 'systemcore/events.html', {})
def gallery(request):
    """
    View function for the gallery page of the site.
    This view renders the gallery.html template and can be used to display
    a collection of images, videos, or other media related to the site or its content,
    allowing users to view and appreciate visual content that enhances their experience.
    """
    return render(request, 'systemcore/gallery.html', {})
def testimonials(request):
    """
    View function for the testimonials page of the site.
    This view renders the testimonials.html template and can be used to display
    feedback or reviews from users or customers, showcasing their experiences with the site, 
    products, or services, and helping to build trust and credibility with potential users.
    """
    return render(request, 'systemcore/testimonials.html', {})       