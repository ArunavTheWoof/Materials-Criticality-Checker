from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_ratings(form_data):
    # Impact on Total Production
    prod_impact_scores = {
        "No Effect": 3,
        "Local Impact": 12,
        "Entire Production Stops": 15
    }
    
    # % Loss of Total Production
    loss_scores = {
        "Nil": 2.5,
        "<=50%": 10,
        ">50%": 12.5
    }
    
    # Lead Time
    lead_time_scores = {
        "<1m": 2,
        "1-3m": 8,
        ">3m": 10
    }
    
    # Impact on Environment
    env_impact_scores = {
        "No Effect": 1.5,
        "Injury or Deviation to Regulation": 6,
        "Fatal or Breach of Regulation": 7.5
    }
    
    # Nature of Item
    nature_scores = {
        "Standard": 1,
        "OEM/Proprietary": 4,
        "Custom": 5
    }
    
    try:
        # Calculate total rating
        total_rating = (
            prod_impact_scores[form_data['prod_impact']] +
            loss_scores[form_data['loss_prod']] +
            lead_time_scores[form_data['lead_time']] +
            env_impact_scores[form_data['env_impact']] +
            nature_scores[form_data['nature']]
        )
        
        # Determine criticality
        if total_rating >= 37.5:
            criticality = "Highly Critical"
            item_class = "X"
        elif total_rating >= 29.5:
            criticality = "Medium Critical"
            item_class = "Y"
        else:
            criticality = "Low Critical"
            item_class = "Z"
            
        return {
            'matl_code': form_data['matl_code'],
            'matl_desc': form_data['matl_desc'],
            'total_rating': total_rating,
            'criticality': criticality,
            'item_class': item_class
        }
    except Exception as e:
        print(f"Error in calculation: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = {
            'matl_code': request.form.get('matl_code'),
            'matl_desc': request.form.get('matl_desc'),
            'prod_impact': request.form.get('prod_impact'),
            'loss_prod': request.form.get('loss_prod'),
            'lead_time': request.form.get('lead_time'),
            'env_impact': request.form.get('env_impact'),
            'nature': request.form.get('nature'),
            'chance_failure': request.form.get('chance_failure'),
            'remarks': request.form.get('remarks')
        }
        result = calculate_ratings(form_data)
        return render_template('index.html', result=result)
    
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
