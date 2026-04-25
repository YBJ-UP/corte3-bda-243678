## ¿Qué política RLS aplicaste a la tabla mascotas?
Pega la cláusula exacta y explica con tus palabras qué hace.
## Cualquiera que sea la estrategia que elegiste para identificar al veterinario actual en RLS, tiene un vector de ataque posible. ¿Cuál es? ¿Tu sistema lo previene? ¿Cómo?
## Si usas SECURITY DEFINER en algún procedure, ¿qué medida específica tomaste para prevenir la escalada de
privilegios que ese modo habilita? Si no lo usas, justifica por qué no era necesario.
## ¿Qué TTL le pusiste al caché Redis y por qué ese valor específico? ¿Qué pasaría si fuera demasiado bajo? ¿Demasiado alto?
## Tu frontend manda input del usuario al backend.
Elige un endpoint crítico y pega la línea exacta donde el backend
maneja ese input antes de enviarlo a la base de datos. Explica qué protege esa línea y de qué. Indica archivo y número
de línea.
## Si revocas todos los permisos del rol de veterinario excepto SELECT en mascotas, ¿qué deja de funcionar en tu sistema?
Lista tres operaciones que se romperían.