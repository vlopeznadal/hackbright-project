$('.edit_review').on('click', editReview);

function editReview() {
    $('#edit_form').html('<form id="updating" action="/updating" method="POST"><div class="mb-3"><label for="rating" class="form-label">Rating</label><input type="range" class="form-range" min="1" max="5" id="rating" name="rating"> <label for="review" class="form-label">Review</label><textarea class="form-control" id="review" rows="3" name="review"></textarea></div><button type="submit" class="btn btn-primary">Submit</button></form>');
}