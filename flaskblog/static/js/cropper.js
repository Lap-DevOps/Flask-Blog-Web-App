const fileInput = document.getElementById("myImageField");
const imagePreview = document.getElementById("selected-image");

const cropper = new Cropper(imagePreview, {
  aspectRatio: 1,
  viewMode: 0,
});

fileInput.addEventListener("change", function (event) {
  const selectedFiles = event.target.files;
  if (selectedFiles.length > 0) {
    const file = selectedFiles[0];

    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      cropper.replace(e.target.result);
    };

    reader.readAsDataURL(file);
  }
});

var submitButton = document.getElementById("cropButton");

submitButton.addEventListener("click", function (event) {
  // Находим скрытое поле binary_data по его id
  var binaryDataField = document.getElementById("cropData");

  // Получаем обрезанное изображение в виде base64-строки
  var croppedImage = cropper.getCroppedCanvas().toDataURL("image/jpeg");

  // Присваиваем значение скрытому полю binaryDataField
  binaryDataField.value = croppedImage;
});


