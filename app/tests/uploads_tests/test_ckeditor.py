import json
from io import BytesIO

import pytest
from PIL import Image

from grandchallenge.uploads.models import UploadModel
from tests.utils import get_view_for_user


@pytest.mark.django_db
def test_upload_with_ckeditor_json(client, TwoChallengeSets):
    filename = "hello.jpg"
    img = BytesIO()
    Image.new("1", (1, 1)).save(img, format="jpeg")
    img.seek(0)
    img.name = filename
    num_files = UploadModel.objects.all().count()
    response = get_view_for_user(
        viewname="uploads:ck-create",
        challenge=TwoChallengeSets.ChallengeSet1.challenge,
        user=TwoChallengeSets.admin12,
        client=client,
        method=client.post,
        data={"upload": img},
        format="multipart",
    )
    retdata = json.loads(response.content)
    assert response.status_code == 200
    assert int(retdata["uploaded"]) == 1
    assert TwoChallengeSets.ChallengeSet1.challenge.short_name in retdata["url"]
    assert (
        TwoChallengeSets.ChallengeSet1.challenge.short_name
        in retdata["fileName"]
    )
    assert UploadModel.objects.all().count() == num_files + 1
    # Check the file is listed in the correct challenge
    response = get_view_for_user(
        viewname="uploads:list",
        challenge=TwoChallengeSets.ChallengeSet1.challenge,
        user=TwoChallengeSets.ChallengeSet1.admin,
        client=client,
    )
    assert retdata["url"] in response.rendered_content
    response = get_view_for_user(
        viewname="uploads:list",
        challenge=TwoChallengeSets.ChallengeSet2.challenge,
        user=TwoChallengeSets.ChallengeSet2.admin,
        client=client,
    )
    assert retdata["url"] not in response.rendered_content
