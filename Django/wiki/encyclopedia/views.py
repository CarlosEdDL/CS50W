from django.shortcuts import render, redirect
import markdown
from . import util




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
    })
def entries(request, entry):
    
    markdown_text = util.get_entry(entry)
    if markdown_text is not None:
        html_text = markdown.markdown(markdown_text)
        return render(request, "encyclopedia/entries.html", {
            "entry_text": html_text,
            "entry": entry })
        
    else:
         return render(request, "encyclopedia/error.html", {
            "message" : "There is not such entry"
         })

  


def new_entry(request):
    if request.method == 'POST':
        entries = util.list_entries
        content = request.POST.get('content').strip()
        title = request.POST.get('title').strip()
        titleInEntry = util.get_entry(title)
        if titleInEntry is not None:
            return render(request, "encyclopedia/error.html", {
                "message": f"The entry for {title} already exists"
                
            })
        else:
            util.save_entry(title,bytes(content, 'utf8'))
            return redirect('index')
        
    return render(request, "encyclopedia/new_entry.html")
        

def search_entry(request):
    recommendations = []
    entries = util.list_entries()
    querys = request.GET.get('q')
    query = querys.strip()
    content = util.get_entry(query)
    if content is not None:
        return redirect(f'/wiki/{query}')
    else:
        for entry in entries:
            if query.lower() in entry.lower():
                recommendations.append(entry)
        if len(recommendations) > 0:
            return render(request, "encyclopedia/recommendations.html", {
            "recommendations": recommendations
        })
        else: 
            return render(request, "encyclopedia/error.html", {
                "message": "No entries found"
            })
            
        


        


def edit(request):
    
    if request.method == 'POST':
        entry = request.POST.get('q')
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit_entry.html", {
            "entry": entry,
            "content": content
        })
    return redirect('index')
        
        


