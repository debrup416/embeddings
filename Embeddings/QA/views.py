from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from QA.models import Qa
from QA.serializers import QaSerializer
from .QuestionAnswer import answer_question


@api_view(['GET', 'POST'])
def qa_list(request,format=None):
    if request.method == 'GET':
        qa = Qa.objects.all()
        serializer = QaSerializer(qa, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        question=request.data['question']
        answer=answer_question(question)
        
        obj={"question":question,"answer":answer}
        serializer = QaSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(obj, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


