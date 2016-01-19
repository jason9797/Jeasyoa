# Jeasyoa
just for learn


if you want to copy image into content ,need to do something:
(1).find the django-ckeditor's package, enter ckeditor-uploader
open urls.py

     url(r'^parseupload/', login_required(views.parseupload), name='ckeditor_parseupload'), into urlpatterns, remember import login_required.

save
#(2).open views.py
add code as follow
     class ImagePasteUploadView(ImageUploadView):

          def post(self, request, **kwargs):
          """
          Uploads a file and send back its URL to CKEditor.
          """
               uploaded_file = request.FILES['upload']
               backend = image_processing.get_backend()
               saved_path = self._save_file(request, uploaded_file)
               self._create_thumbnail_if_needed(backend, saved_path)
               url = utils.get_media_url(saved_path)
               return JsonResponse({'uploaded': 1, 'fileName': 'filename.jpg', 'url': url})
          #upload = csrf_exempt(ImageUploadView.as_view())
          parseupload = csrf_exempt(ImagePasteUploadView.as_view())
save
#(3).make sure settings.py(Jeasyoa's path)
'filebrowserUploadUrl' value equal to fist step url added.

