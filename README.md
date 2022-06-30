# clinica 
Relational schema
architecture
it is a backend system for the operation of clinics

architecture
============
![relational schema](/conections.png)

usage
=====
Django tried these URL patterns, in this orde
> - admin/
> - api-auth/  
> - client/  
> - client<drf_format_suffix:format>  
> - client/<int:pk>  
> - client/<int:pk><drf_format_suffix:format  
> - worker/  
> - worker<drf_format_suffix:format  
> - worker/<int:pk>  
> - worker/<int:pk><drf_format_suffix:format  
> - service  
> - service<drf_format_suffix:format  
> - service/<int:pk>  
> - service/<int:pk><drf_format_suffix:format  
> - location/  
> - location<drf_format_suffix:format  
> - location/<int:pk>/  
> - location/<int:pk><drf_format_suffix:format  
> - appointement/  
> - appointement<drf_format_suffix:format  
> - appointement/<int:pk>  
> - appointement/<int:pk><drf_format_suffix:format  
> - user/  
> - user<drf_format_suffix:format  
> - user/<int:pk>/  
> - user/<int:pk><drf_format_suffix:format  
> - register/  
> - register<drf_format_suffix:format>

	
