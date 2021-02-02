from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list=Category.objects.order_by('-likes')[:5]
    pages_list=Page.objects.order_by('-views')[:5]

    context_dict={}
    context_dict['boldmessage']='Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories']=category_list
    context_dict['pages']=pages_list
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use
    return render(request,'rango/index.html', context=context_dict)
    
    

def about(request):
    return render(request,'rango/about.html')
    
def show_category(request, category_name_slug):
    context_dict={}

    try:
        category=Category.objects.get(slug=category_name_slug)
        pages=Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['category']=None
        context_dict['pages']=None
    
    return render(request,'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    #A HTTP POST?
    if request.method =='POST':
        form=CategoryForm(request.POST)
        
        #Have we been provided with a valid form?
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else: 
            print (form.errors)
    #We will handle the bad form, new form, or no form supplied cases/
    #Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form':form})
