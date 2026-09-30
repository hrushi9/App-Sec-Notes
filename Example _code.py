from flask import Flask, request, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 88104, "userId": 1042, "status": "shipped"},
    {"id": 88090, "userId": 1042, "status": "shipped"},
    {"id": 88071, "userId": 1042, "status": "pending"},
    {"id": 88052, "userId": 1042, "status": "delivered"},
    {"id": 88031, "userId": 1042, "status": "shipped"},
    {"id": 88020, "userId": 1042, "status": "cancelled"},
]

# Parameters
@app.route("/api/v1/orders", methods=["GET"])
def get_orders():

    status = request.args.get("status")

    limit = request.args.get(
        "limit",
        default=10,
        type=int
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    # Validation
    if limit < 1 or limit > 100:
        return jsonify({
            "error": "limit must be between 1 and 100"
        }), 400

    if page < 1:
        return jsonify({
            "error": "page must be greater than 0"
        }), 400

    # Filtering
    filtered_orders = ORDERS

    if status:
        filtered_orders = [
            order
            for order in ORDERS
            if order["status"] == status
        ]

    # Counting
    total_count = len(filtered_orders)

    # Pagination
    offset = (page - 1) * limit

    paginated_orders = filtered_orders[
        offset: offset + limit
    ]

    # Navigation
    if offset + limit < total_count:
        next_url = (
            f"/api/v1/orders?"
            f"status={status}&"
            f"limit={limit}&"
            f"page={page + 1}"
        )
    else:
        next_url = None

    # Response
    response = jsonify({
        "data": paginated_orders,
        "page": page,
        "limit": limit,
        "next": next_url
    })

    response.headers["X-Total-Count"] = str(total_count)

    return response, 200


if __name__ == "__main__":
    app.run(debug=True)
