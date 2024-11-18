import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "posts/index.html")

# Function for infinite scroll.
def posts(request):

    # need to provide 2 arguments.
    # Get start and end points
    # "http://127.0.0.1:8000/posts?start=1&end=10"

    # the "start" and "end" in .get comes from the URL

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    # Generate list of dummy posts
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    """ Output (JSON):
    {"posts": ["Post #1", "Post #2", "Post #3", "Post #4", "Post #5", "Post #6", "Post #7", "Post #8", "Post #9", "Post #10"]}
    """
    # Artificially delay speed of response
    time.sleep(1)

    # Return list of posts
    return JsonResponse({
        "posts": data
    })