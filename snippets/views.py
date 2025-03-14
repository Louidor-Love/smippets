from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db import IntegrityError
from .models import Language,Snippet,UserProfile
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SnippetForm


# class SnippetAdd(View):
#    TODO: Implement this class to handle snippet creation, only for authenticated users.
class  SnippetAdd(View):
    def get(self, request, *args, **kwargs):
        return render (request,'snippets/snippet_add.html',{'form':SnippetForm})

    def post(self,request,*args,**kwargs):
        form = SnippetForm(request.POST)
        if form.is_valid():  # Validar el formulario
            try:
                snippet = form.save(commit=False)  # No guarda en la BD todavía
                snippet.user = request.user  # Asigna el usuario actual
                snippet.save()  # Guarda el snippet con el usuario asignado
                messages.success(request, "Snippet creado correctamente.")  # Mensaje de éxito
                return redirect('index')  # Redirige a la lista de snippets
            except IntegrityError:
                messages.error(request, "Error: No se pudo guardar el snippet. Verifica los datos ingresados.")  # Mensaje de error
    

# class SnippetEdit(View):
#    TODO: Implement this class to handle snippet editing. Allow editing only for the owner.
class SnippetEdit(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        snippet =  get_object_or_404(Snippet,id=snippet_id)

        if snippet.user != request.user:
            messages.error(request, "No tienes permiso para editar este snippet.")
            return redirect('index')

        form = SnippetForm(instance=snippet)    

        return render (request,'snippets/snippet_add.html',{'form':form})

    def post(self,request,*args,**kwargs):
        snippet_id = self.kwargs["id"] 
        snippet = get_object_or_404(Snippet, id=snippet_id) 
        form = SnippetForm(request.POST, instance=snippet)

        if snippet.user != request.user: 
            messages.error(request, "No tienes permiso para editar este snippet.")
            return redirect("index")

        if form.is_valid():  
            try:
                form.save() 
                messages.success(request, "Snippet actualizado correctamente.") 
                return redirect('index') 
            except IntegrityError:
                messages.error(request, "Error: No se pudo guardar el snippet. Verifica los datos ingresados.") 
        else:
            messages.error(request, "Error en el formulario. Por favor, verifica los campos.")
            return render(request, 'snippets/snippet_add.html', {'form': form})



# class SnippetDelete(View):
#    TODO: Implement this class to handle snippet deletion. Allow deletion only for the owner.
class SnippetDelete(View):
    def post(self,request,*args,**kwargs):
        snippet_id = self.kwargs["id"] 
        snippet = get_object_or_404(Snippet, id=snippet_id) 

        if snippet.user != request.user: 
            messages.error(request, "No tienes permiso para editar este snippet.")
            return redirect("index")

        snippet.delete()
        messages.success(request, "Snippet borrado correctamente.") 

        return redirect("index")


class SnippetDetail(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        # TODO: Implement logic to get snippet by ID
        snippet = Snippet.objects.get(id=snippet_id)
        # Add conditions for private snippets
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )  # Placeholder

class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except Snippet.DoesNotExist:
            raise Http404("Snippet no encontrado")
        
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )  # Placeholder

      


class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        # TODO: Fetch user snippets based on username and public/private logic
        profile = get_object_or_404(UserProfile, slug=username)
        snippets = Snippet.objects.filter(user=profile.user)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": profile.user.username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        # TODO: Fetch snippets based on language
        return render(request, "index.html", {"snippets": []})  # Placeholder


class Index(View):
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})  # Placeholder


# class Login(View):
#    TODO: Implement login view logic with AuthenticationForm and login handling.
class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'form': AuthenticationForm()})

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                "error": "Nombre de usuario o Contraseña incorrecto"
            })
        else:
            login(request, user)
            return redirect('index')


# class Logout(View):
#    TODO: Implement logout view logic.
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
