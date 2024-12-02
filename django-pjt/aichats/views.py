# movie/views.py
import openai
from django.conf import settings
from django.http import JsonResponse

# OpenAI API 키를 설정 (settings.py에 설정된 API 키 사용)
openai.api_key = settings.OPENAI_API_KEY

def get_scene_location(request):
    if request.method == "POST":
        # 클라이언트로부터 받은 영화 장면 설명
        scene_description = request.POST.get('scene_description')
        
        if not scene_description:
            return JsonResponse({'error': 'Scene description is required'}, status=400)

        try:
            # OpenAI API 호출 (GPT 모델 사용)
            response = openai.Completion.create(
                model="gpt-4-mini",  # 사용하고자 하는 GPT 모델 선택
                prompt=f"Describe the location in the following movie scene: {scene_description}",
                max_tokens=100
            )
            
            location = response.choices[0].text.strip()
            
            return JsonResponse({'location': location})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
