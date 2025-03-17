from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.views import View
from django.contrib import messages
from django.db import IntegrityError
from .models import Language,Snippet,UserProfile
from django.http import Http404
from django.shortcuts import render, redirect
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import SnippetForm
from django.conf import settings


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

                #manejo el mail
                subject = snippet.name 
                body = snippet.description

                # Aquí puedes configurar el correo
                message_html = render_to_string(
                    'snippets/email.html',  # Plantilla del correo (opcional)
                    {'snippet_name': snippet.name, 'snippet_description': snippet.description}
                )

                # Crea el objeto EmailMessage
                email =  EmailMultiAlternatives(
                    subject=subject,
                    body=message_html,
                    from_email=settings.EMAIL_HOST_USER,  # Correo del remitente
                    to=[settings.PERSONAL_EMAIL],  # Correo del destinatario
                )
                email.attach_alternative(message_html, "text/html")
                email.send(fail_silently=False)  # Enviar el correo
                messages.success(request, "Snippet creado correctamente.")  # Mensaje de éxito
                return redirect('index')  # Redirige a la lista de snippets
            except IntegrityError:
                messages.error(request, "Error: No se pudo guardar el snippet. Verifica los datos ingresados.")  # Mensaje de error
    

# class SnippetEdit(View):
#    TODO: Implement this class to handle snippet editing. Allow editing only for the owner.
class SnippetEdit(LoginRequiredMixin,View):
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


class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        # TODO: Implement logic to get snippet by ID
        snippet = Snippet.objects.get(id=snippet_id)

        language_slug = snippet.language.slug

        lexer = get_lexer_by_name(language_slug)
        formatter = HtmlFormatter(linenos=True, full=True)  
        highlighted_code = highlight(snippet.snippet, lexer, formatter)
        # Add conditions for private snippets
        return render(
            request, "snippets/snippet.html", {"snippet": snippet,"highlighted_code": highlighted_code}
        )  # Placeholder

class SnippetDetail(View):
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

        if request.user == profile.user:
            snippets = Snippet.objects.filter(user=profile.user)
        else:
            snippets = Snippet.objects.filter(user=profile.user, public=True)   
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": profile.user.username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        language = get_object_or_404(Language, slug=language)
        snippets = Snippet.objects.filter(language=language, public=True)
        # TODO: Fetch snippets based on language
        return render(request, "snippets/snippets_lang.html", {"snippets": snippets, "language": language})  # Placeholder


class Index(View):
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        if request.user.is_authenticated:
            snippets = Snippet.objects.filter(Q(public=True) | Q(user=request.user))
        else:
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
