import os
import subprocess
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Subtitle
from django.http import JsonResponse

def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES['video_file']
        video = Video.objects.create(video_file=video_file, title=video_file.name)
        
        # Extract subtitles using ffmpeg
        video_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
        subtitle_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', f"{video.title}.srt")
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'subtitles'), exist_ok=True)
        
        # ffmpeg command to extract subtitles
        command = f"ffmpeg -i {video_path} -map 0:s:0 {subtitle_path}"
        subprocess.run(command, shell=True)

        # Read the generated SRT file and store subtitles in the database
        with open(subtitle_path, 'r') as f:
            subtitles = parse_srt(f.read())
            for sub in subtitles:
                Subtitle.objects.create(video=video, timestamp=sub['timestamp'], content=sub['content'])
        
        return redirect('video_list')

    return render(request, 'videoapp/upload.html')

from django.shortcuts import render, get_object_or_404
from .models import Video
from django.conf import settings
import os

import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Video

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Generate subtitle file URL
    subtitle_filename = f"{os.path.splitext(os.path.basename(video.video_file.name))[0]}.srt"
    subtitle_file_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', subtitle_filename)
    subtitle_file_url = os.path.join(settings.MEDIA_URL, 'subtitles', subtitle_filename)
    
    # Check if the subtitle file exists
    if not os.path.exists(subtitle_file_path):
        subtitle_file_url = None

    return render(request, 'videoapp/video_detail.html', {
        'video': video,
        'subtitle_file_url': subtitle_file_url
    })






# Helper function to parse SRT file
def parse_srt(srt_content):
    subtitles = []
    for block in srt_content.strip().split('\n\n'):
        lines = block.split('\n')
        if len(lines) >= 3:
            timestamp = lines[1].split(' --> ')[0].strip()  # Start timestamp
            content = ' '.join(lines[2:])
            subtitles.append({'timestamp': timestamp, 'content': content})
    return subtitles

#Adding search functionality
def search_subtitle(request):
    query = request.GET.get('q')
    video_id = request.GET.get('video_id')
    subtitles = Subtitle.objects.filter(video_id=video_id)

    matches = []
    for subtitle in subtitles:
        if query.lower() in subtitle.content.lower():
            matches.append({
                'timestamp': subtitle.timestamp,
                'content': subtitle.content
            })

    return JsonResponse(matches, safe=False)

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videoapp/video_list.html', {'videos': videos})
