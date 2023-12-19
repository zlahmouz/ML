function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples
% You need to return the following variables correctly 
h=X*theta;
J = sum((h-y).^2)/(2*m)+(lambda*sum(theta(2:end).^2))/(2*m);
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%


grad= (lambda/m)*[0;theta(2:end)] ;
reg=(1/m)*X'*(h-y);
grad=grad+reg;


% Step 3: Compute the Gradient (grad)
% Compute the gradient for the unregularized cost
%grad_unregularized = (1 / m) * (X' * (h - y));

% Compute the regularization term for the gradient
%reg_term_grad = (lambda / m) * [0; theta(2:end)]; % 0 for theta(1), lambda * theta(j) for j > 1

% Add the regularization term to the gradient
%grad = grad_unregularized + reg_term_grad;






% =========================================================================

grad = grad(:);

end
